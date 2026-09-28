# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/
# verified.

import asyncio

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ContextPrecision

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "llama3.2"


def build_scorer() -> tuple[ContextPrecision, AsyncOpenAI]:
    """Create an Ollama-backed LLM and the ContextPrecision metric."""
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama ignores the key, but the client requires one
        base_url=OLLAMA_BASE_URL,
    )
    llm = llm_factory(MODEL_NAME, provider="openai", client=client)
    return ContextPrecision(llm=llm), client


async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(
            user_input="Where is the Eiffel Tower located?",
            reference="The Eiffel Tower is located in Paris.",
            retrieved_contexts=[
                "The Eiffel Tower is located in Paris.",
                "The Brandenburg Gate is located in Berlin.",
            ],
        )
        print(f"Context Precision Score: {result.value}")
    finally:
        await client.close()  # avoids "unclosed client" warnings on exit


if __name__ == "__main__":
    asyncio.run(main())