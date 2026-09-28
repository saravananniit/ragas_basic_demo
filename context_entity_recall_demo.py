# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_entities_recall/
# verified, How to change Model parameter for ollama - llama3.1:8b
# Create a Model file

# FROM llama3.1:8b
# PARAMETER num_ctx 8192
# PARAMETER temperature 0

# ollama create llama3.1-8k -f Modelfile


import asyncio

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextEntityRecall

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "llama3.1-8k"


def build_scorer() -> tuple[ContextEntityRecall, AsyncOpenAI]:
    """Create an Ollama-backed LLM and the ContextEntityRecall metric."""
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama ignores the key, but the client requires one
        base_url=OLLAMA_BASE_URL,
    )
    llm = llm_factory(MODEL_NAME, provider="openai", client=client)
    return ContextEntityRecall(llm=llm), client


async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(
            reference="The Eiffel Tower is located in Paris.",
            retrieved_contexts=["The Eiffel Tower is located in Paris."],
        )
        print(f"Context Entity Recall Score: {result.value}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())