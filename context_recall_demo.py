# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/
# verified
import asyncio

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextRecall

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "qwen2.5:7b"


def build_scorer() -> tuple[ContextRecall, AsyncOpenAI]:
    """Create an Ollama-backed LLM and the ContextRecall metric."""
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama ignores the key, but the client requires one
        base_url=OLLAMA_BASE_URL,
    )
    llm = llm_factory(MODEL_NAME, provider="openai", client=client)
    return ContextRecall(llm=llm), client


async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(
            user_input="Where is the Eiffel Tower located?",
            retrieved_contexts=["Paris is the capital of France."],
            reference="The Eiffel Tower is located in Paris.",
        )
        print(f"Context Recall Score: {result.value}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())