from NN.Text_summarization_service.Config_files.Prompts import get_prompt_for_summary
from langchain_core.prompts import PromptTemplate
from google import genai


class GeminiGeneration:
    def __init__(self, api_key: str, model_name: str):
        self._client = genai.Client(api_key=api_key)
        self._model_name = model_name
        self._content = ""

    def generate(self, text_to_summarize: str) -> str:

        summary_prompt, instruction = get_prompt_for_summary()
        summary_prompt = PromptTemplate.from_template(summary_prompt)

        self._content = summary_prompt.format(instruction=instruction, input_text=text_to_summarize)

        chat_response = self._client.models.generate_content(
            model=self._model_name,
            contents=self._content
        )

        return chat_response.text