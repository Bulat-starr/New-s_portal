from vllm import LLM, SamplingParams


class ModelLocalInferenceVLLM:
    def __init__(self, model_name='RefalMachine/RuadaptQwen2.5-1.5B-instruct',
                 temperature=0.8, top_p=0.95, top_k=10, min_tokens=40, max_tokens=100, ignore_eos=True):

        self._model_name = model_name
        self._sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            ignore_eos=ignore_eos,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
        )

        self._llm = LLM(model_name=model_name)


    @staticmethod
    def _convert_text_to_prompt(texts) -> list:
        """Converts the input list of texts into a list of model-appropriate prompts"""
        prompts = [f"USER: \n{content}\nASSISTANT:" for content in texts]
        return prompts

    def inference(self, texts: list[str]) -> list[str]:
        """Generate summary for input texts"""
        converted_texts = self._convert_text_to_prompt(texts)
        outputs = self._llm.generate(converted_texts, self._sampling_params)

        output_array = []
        for output in outputs:
            output_array.append(output.outputs[0].text)

        return output_array
