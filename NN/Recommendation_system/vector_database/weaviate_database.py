import os
import weaviate
from weaviate.auth import Auth
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from weaviate.classes.config import Property, DataType, Configure


weaviate_url = "un3wjnomqgeos99guzariq.c0.europe-west3.gcp.weaviate.cloud"
waeviate_api_key = "Y2JuSThKK1ZReEVaZFZISF9DTitqOXN0TlloMUhkbVlyZnlkQUJ0S3g3TXdkTTV2WDM1WkFIYmIzVjhZPV92MjAw"



class WeaviateDatabase:
    def __init__(self, weaviate_url_address: str,
                 weaviate_api_key: str,
                 model_name="intfloat/multilingual-e5-small",
                 batch_size=128):

        self._client = weaviate.connect_to_weaviate_cloud(
                  cluster_url=weaviate_url_address,
                  auth_credentials=Auth.api_key(weaviate_api_key),
              )
        self._create_collections()
        self._collection = self._client.collections.get("hackathon_database")

        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModel.from_pretrained(model_name).eval().to(self._device)

        self._batch_size = batch_size

    @staticmethod
    def _average_pool(last_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        embeddings = F.normalize(last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None], p=2, dim=1)
        return embeddings

    def _create_collections(self):
        self._client.collections.create(
            "hackathon_database",
            properties=[
                Property(name="text", data_type=DataType.TEXT),
            ]
        )

    def add_texts_to_weaviate_database(self, texts: list[str]):
        for i in tqdm(range(0, len(texts), self._batch_size)):
            batch_contexts = texts[i:i + self._batch_size]

            batch_dict = self._tokenizer(
                ["passage: " + c for c in batch_contexts],
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

            with self._collection.batch.dynamic() as batch:
                for j, context in enumerate(batch_contexts):
                    batch.add_object(
                        properties={
                            "text": context,
                        },
                        vector=embeddings[j].tolist()
                    )

    def semantic_search(self, query):
        query_dict = self._tokenizer(
            "query: " + query,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt',
        ).to(self._device)

        with torch.no_grad():
            outputs = self._model(**query_dict)

        query_embedding = self._average_pool(outputs.last_hidden_state, query_dict['attention_mask'])
        query_embedding = F.normalize(query_embedding, p=2, dim=1)

        response = self._collection.query.near_vector(
            near_vector=query_embedding.tolist()[0],
            limit=3
        )
        output_array = []
        for item in response.objects:
            output_array.append(item.properties["text"])

        return output_array


cluster = WeaviateDatabase(weaviate_url, waeviate_api_key)