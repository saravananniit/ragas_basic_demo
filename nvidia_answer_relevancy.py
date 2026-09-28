# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/nvidia_metrics/#answer-accuracy
# verified

import asyncio

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerAccuracy

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "llama3.2:latest"


def build_scorer() -> tuple[AnswerAccuracy, AsyncOpenAI]:
    """Create an Ollama-backed LLM and the AnswerAccuracy metric."""
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama ignores the key, but the client requires one
        base_url=OLLAMA_BASE_URL,
    )
    llm = llm_factory(MODEL_NAME, provider="openai", client=client)
    return AnswerAccuracy(llm=llm), client


async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(
            user_input="When was Einstein born?",
            response="Albert Einstein was born in 1879.",
            reference="Albert Einstein was born in 1879.",
        )
        print(f"Answer Accuracy Score: {result.value}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())