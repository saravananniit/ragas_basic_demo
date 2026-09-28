# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/answer_relevance/

import asyncio
import os

from openai import AsyncAzureOpenAI
from ragas.embeddings.base import embedding_factory
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy

# ---------------------------------------------------------------------------
# Configuration (Azure AI Foundry)
# ---------------------------------------------------------------------------
# AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]        # Keys and Endpoint in Foundry
# AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]      # e.g. https://<resource>.openai.azure.com/
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

# # Deployment names (Deployments page in Foundry), not base model names.
# # Defaults assume you named the deployments after the models.
# LLM_DEPLOYMENT = os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT", "gpt-4o-mini")
# EMBED_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small")


# ---------------------------------------------------------------------------
# LLM + embeddings + metric setup
# ---------------------------------------------------------------------------
def build_scorer() -> tuple[AnswerRelevancy, AsyncAzureOpenAI]:
    """Create Azure-backed LLM + embeddings and the AnswerRelevancy metric."""
    client = AsyncAzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
    )
    llm = llm_factory(LLM_DEPLOYMENT, provider="openai", client=client)
    embeddings = embedding_factory("openai", model=EMBED_DEPLOYMENT, client=client)
    return AnswerRelevancy(llm=llm, embeddings=embeddings), client


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
SAMPLE = {
    "user_input": "When was the first super bowl?",
    "response": "The first superbowl was held on Jan 15, 1967",
}


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
async def main() -> None:
    scorer, client = build_scorer()
    try:
        result = await scorer.ascore(**SAMPLE)
        print(f"Answer Relevancy Score: {result.value}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())  # in a notebook, just use: await main()

