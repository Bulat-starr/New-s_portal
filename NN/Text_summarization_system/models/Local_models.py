from vllm import LLM, SamplingParams
from NN.Recommendation_system.vector_database.weaviate_database import WeaviateDatabase
from News.app.Backend.API_news_services.news.models.article_struct import article

class ModelLocalInferenceVLLM:
    def __init__(self, weaviate_url, weaviate_api_key,
                 model_name='RefalMachine/RuadaptQwen2.5-1.5B-instruct',
                 temperature=0.8,
                 top_p=0.95,
                 top_k=10,
                 min_tokens=40,
                 max_tokens=100,
                 ignore_eos=True,
                 ):

        self._model_name = model_name
        self._sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            ignore_eos=ignore_eos,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
        )

        self._llm = LLM(model=model_name)
        self._weaviate_db = WeaviateDatabase(weaviate_url, weaviate_api_key)


    @staticmethod
    def _convert_text_to_prompt(articles: list[article]) -> list:
        """Converts the input list of texts into a list of model-appropriate prompts"""
        prompts = [f"USER: \n{content.getContent()}\nASSISTANT:" for content in articles]
        return prompts

    def inference(self, articles: list[article]) -> None:
        """Generate summary for input texts"""
        converted_texts = self._convert_text_to_prompt(articles)
        outputs = self._llm.generate(converted_texts, self._sampling_params)

        summary = []
        for output in outputs:
            summary.append(output.outputs[0].text)

        self._weaviate_db.add_texts_to_weaviate_database(summary, articles)
