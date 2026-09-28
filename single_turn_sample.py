# # https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/#legacy-metrics-api
# import asyncio

# from langchain_openai import ChatOpenAI
# from ragas import SingleTurnSample
# from ragas.llms import LangchainLLMWrapper
# from ragas.metrics import LLMContextPrecisionWithoutReference

# OLLAMA_BASE_URL = "http://localhost:11434/v1"
# MODEL_NAME = "llama3.2:latest"


# def build_metric() -> LLMContextPrecisionWithoutReference:
#     """Create an Ollama-backed evaluator LLM and the metric."""
#     evaluator_llm = LangchainLLMWrapper(
#         ChatOpenAI(
#             model=MODEL_NAME,
#             api_key="ollama",  # Ollama ignores the key, but the client requires one
#             base_url=OLLAMA_BASE_URL,
#             temperature=0,
#         )
#     )
#     return LLMContextPrecisionWithoutReference(llm=evaluator_llm)


# async def main() -> None:
#     context_precision = build_metric()

#     sample = SingleTurnSample(
#         user_input="Where is the Eiffel Tower located?",
#         response="The Eiffel Tower is located in Paris.",
#         retrieved_contexts=["The Eiffel Tower is located in Paris."],
#     )

#     score = await context_precision.single_turn_ascore(sample)
#     print(f"Context Precision (without reference): {score}")


# if __name__ == "__main__":
#     asyncio.run(main())