# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/nvidia_metrics/#response-groundedness
# verified

import asyncio
import os

from openai import AsyncAzureOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ResponseGroundedness

# ---------------------------------------------------------------------------
# Configuration (Azure AI Foundry)
# ---------------------------------------------------------------------------
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]        # Keys and Endpoint in Foundry
AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]      # e.g. https://<resource>.openai.azure.com/
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]  # Deployment name, not the base model name


# ---------------------------------------------------------------------------
# LLM + metric setup
# ---------------------------------------------------------------------------
def build_scorer() -> tuple[ResponseGroundedness, AsyncAzureOpenAI]:
    """Create an Azure-backed LLM and the ResponseGroundedness metric."""
    client = AsyncAzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
    )
    llm = llm_factory(AZURE_OPENAI_DEPLOYMENT, provider="openai", client=client)
    return ResponseGroundedness(llm=llm), client


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
SAMPLE = {
    "response": "Albert Einstein was born in 1879.",
    "retrieved_contexts": [
        "Albert Einstein was born March 14, 1879.",
        "Albert Einstein was born at Ulm, in Württemberg, Germany.",
    ],
}


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(**SAMPLE)
        print(f"Response Groundedness Score: {result.value}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())  # in a notebook, just use: await main()