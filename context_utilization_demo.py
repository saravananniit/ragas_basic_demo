# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/#context-utilization
# verified
import asyncio

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextUtilization

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "llama3.2:latest"


def build_scorer() -> tuple[ContextUtilization, AsyncOpenAI]:
    """Create an Ollama-backed LLM and the ContextUtilization metric."""
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama ignores the key, but the client requires one
        base_url=OLLAMA_BASE_URL,
    )
    llm = llm_factory(MODEL_NAME, provider="openai", client=client)
    return ContextUtilization(llm=llm), client


async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(
            user_input="Where is the Eiffel Tower located?",
            response="The Eiffel Tower is located in Paris.",
            retrieved_contexts=[
                "The Eiffel Tower is located in Paris.",
                "The Brandenburg Gate is located in Berlin.",
            ],
        )
        print(f"Context Utilization Score: {result.value}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())