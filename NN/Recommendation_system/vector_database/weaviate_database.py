import math
import random
from News.app.Backend.API_news_services.news.models.article_struct import article
from News.app.app_logging.logger import logger
import weaviate
from weaviate.auth import Auth
from weaviate.classes.config import Property, DataType
from weaviate.classes.query import MetadataQuery
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from threading import Thread
from tqdm import tqdm
import time

class WeaviateDatabase:
    def __init__(self, weaviate_url: str,
                 weaviate_api_key: str,
                 model_name="AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru",
                 batch_size=128,
                 num_workers=4):

        self._weaviate_url_address = weaviate_url
        self._weaviate_api_key = Auth.api_key(weaviate_api_key)

        self._create_collections()

        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModel.from_pretrained(model_name).eval().to(self._device)

        self._batch_size = batch_size
        self._cluster_name = "hackathon_database"
        logger.debug("Weaviate model initialized successfully!")
        print("Weaviate model initialized successfully!")


    @staticmethod
    def _average_pool(last_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        embeddings = F.normalize(last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None], p=2, dim=1)
        return embeddings


    @staticmethod
    def timer(f):
        def tmp(*args, **kwargs):
            t = time.time()
            res = f(*args, **kwargs)
            print("Время выполнения функции: %f" % (time.time() - t))
            logger.debug("Время выполнения функции: %f" % (time.time() - t))
            return res

        return tmp


    def _create_collections(self):
        """Create collection in Weaviate database"""

        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self._weaviate_url_address,
            auth_credentials=self._weaviate_api_key,
        )
        try:
            client.collections.create(
                "hackathon_database",
                properties=[
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="page_title", data_type=DataType.TEXT),
                    Property(name="article_author", data_type=DataType.TEXT),
                    Property(name="text_summary", data_type=DataType.TEXT),
                ]
            )
            client.close()
        except:
            logger.debug("Collection already exists!")
            print("Collection already exists!")
            client.close()


    @staticmethod
    def _get_text_with_max_distance(array_texts) -> str:
        """Find text with minimum cosinus distance"""

        min_cos_distance = 1.0
        text_max_distance = ""
        for text, distance in array_texts:
            if distance < min_cos_distance:
                min_cos_distance = distance
                text_max_distance = text

        logger.debug("Get text with max distance: %f" % min_cos_distance)
        return text_max_distance


    @timer
    def add_texts_to_weaviate_database(self, summaries: list[str], array_articles: list[article]):
        """Add texts with metadata and summary to Weaviate database"""

        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self._weaviate_url_address,
            auth_credentials=self._weaviate_api_key,
        )
        collection = client.collections.get(self._cluster_name)

        for i in tqdm(range(0, len(array_articles), self._batch_size)):
            batch_articles = array_articles[i:i + self._batch_size]

            batch_dict = self._tokenizer(
                ["passage: " + c.getContent() for c in batch_articles],
                max_length=512,
                padding=True,
                truncation=True,
                return_tensors='pt'
            )

            for key in batch_dict.keys():
                batch_dict[key] = batch_dict[key].to(self._device)

            with torch.no_grad():
                outputs = self._model(**batch_dict)

            embeddings = self._average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
            embeddings = F.normalize(embeddings, p=2, dim=1)

            with collection.batch.dynamic() as batch:
                for j, article in enumerate(batch_articles):
                    batch.add_object(
                        properties={
                            "text": article.getContent(),
                            "page_title": article.getTitle(),
                            "page_url": article.getUrl(),
                            "article_author": article.getAuthor(),
                            "text_summary": summaries[j]
                        },
                        vector=embeddings[j].tolist()
                    )
        client.close()


    def _get_sample_from_weaviate_db(self) -> tuple[str, list]:
        """Get random sample from Weaviate database"""

        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self._weaviate_url_address,
            auth_credentials=self._weaviate_api_key,
        )
        collection = client.collections.get(self._cluster_name)
        all_objects = []

        for item in collection.iterator(include_vector=True):
            all_objects.append(item.properties["text"])

        random_element = random.choice(all_objects)
        client.close()

        return random_element


    def get_recommendation_from_db(self, text, return_samples=40, eps=0.5, parts=4):
        """Get recommendations from Weaviate database using semantic similarity"""

        all_samples = []
        limit = math.ceil(return_samples / parts)
        array_texts = []

        for i in range(parts):
            if i == 0:
                array_texts = self._semantic_search(text, limit=limit)
                all_samples.extend(array_texts)
            elif random.random() < eps:
                random_text = self._get_sample_from_weaviate_db()
                array_texts = self._semantic_search(random_text, limit=limit)
                all_samples.extend(array_texts)
            else:
                text_max_distance = self._get_text_with_max_distance(array_texts)
                array_texts = self._semantic_search(text_max_distance, limit=limit)
                all_samples.extend(array_texts)

        random.shuffle(all_samples)
        return all_samples[:return_samples]


    @timer
    def _semantic_search(self, text, limit=3):
        """Using cosinus similarity search"""

        text_dict = self._tokenizer(
            "query: " + text,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt',
        ).to(self._device)

        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self._weaviate_url_address,
            auth_credentials=self._weaviate_api_key,
        )
        collection = client.collections.get(self._cluster_name)

        with torch.no_grad():
            outputs = self._model(**text_dict)

        query_embedding = self._average_pool(outputs.last_hidden_state, text_dict['attention_mask'])
        query_embedding = F.normalize(query_embedding, p=2, dim=1)

        response = collection.query.near_vector(
            near_vector=query_embedding.tolist()[0],
            limit=limit,
            return_metadata=MetadataQuery(distance=True)
        )
        output_articles: list[dict] = []
        for item in response.objects:
            local_dc = dict()
            local_dc["text"] = item.properties["text"]
            local_dc["page_title"] = item.properties["page_title"]
            local_dc["page_url"] = item.properties["page_url"]
            local_dc["article_author"] = item.properties["article_author"]
            local_dc["text_summary"] = item.properties["text_summary"]
            output_articles.append(local_dc)

        client.close()

        return output_articles

    def get_all_data_from_weaviate_db(self):
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self._weaviate_url_address,
            auth_credentials=self._weaviate_api_key,
        )
        collection = client.collections.get(self._cluster_name)
        all_data = []
        for item in collection.iterator():
            all_data.append(item.properties)

        return all_data