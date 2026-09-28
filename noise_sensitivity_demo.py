# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/noise_sensitivity/#example
# verified

import asyncio
import os

from openai import AsyncAzureOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import NoiseSensitivity

# ---------------------------------------------------------------------------
# Configuration (Azure AI Foundry)
# ---------------------------------------------------------------------------
AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]        # Keys and Endpoint in Foundry
AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]      # e.g. https://<resource>.openai.azure.com/
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"] # Deployment name, not the base model name

# ---------------------------------------------------------------------------
# LLM setup
# ---------------------------------------------------------------------------
client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
)
llm = llm_factory(AZURE_OPENAI_DEPLOYMENT, client=client)

# ---------------------------------------------------------------------------
# Metric
# ---------------------------------------------------------------------------
scorer = NoiseSensitivity(llm=llm)

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
SAMPLE = {
    "user_input": "What is the Life Insurance Corporation of India (LIC) known for?",
    "response": (
        "The Life Insurance Corporation of India (LIC) is the largest insurance company "
        "in India, known for its vast portfolio of investments. LIC contributes to the "
        "financial stability of the country."
    ),
    "reference": (
        "The Life Insurance Corporation of India (LIC) is the largest insurance company "
        "in India, established in 1956 through the nationalization of the insurance "
        "industry. It is known for managing a large portfolio of investments."
    ),
    "retrieved_contexts": [
        "The Life Insurance Corporation of India (LIC) was established in 1956 following the nationalization of the insurance industry in India.",
        "LIC is the largest insurance company in India, with a vast network of policyholders and huge investments.",
        "As the largest institutional investor in India, LIC manages substantial funds, contributing to the financial stability of the country.",
        "The Indian economy is one of the fastest-growing major economies in the world, thanks to sectors like finance, technology, manufacturing etc.",
    ],
}

# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
async def main() -> None:
    result = await scorer.ascore(**SAMPLE)
    print(f"Noise Sensitivity Score: {result.value}")


if __name__ == "__main__":
    asyncio.run(main())  # in a notebook, just use: await main()