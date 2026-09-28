# https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/
# verified

import os
import asyncio
from openai import AsyncAzureOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness

client = AsyncAzureOpenAI(
    # api_key=os.environ["AZURE_OPENAI_API_KEY"],          # Keys and Endpoint in Foundry
    # azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],  # e.g. https://<resource>.openai.azure.com/
    # api_version="2024-10-21",  
    
)

# Deployment name from Foundry (Deployments page)
llm = llm_factory("gpt-4o-mini", client=client)

scorer = Faithfulness(llm=llm)

async def main():
    result = await scorer.ascore(
        user_input="When was the first super bowl?",
        response="The first superbowl was held on Jan 15, 1967",
        retrieved_contexts=[
            "The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
        ],
    )
    print(f"Faithfulness Score: {result.value}")

asyncio.run(main())   # in a notebook, just use: await main()