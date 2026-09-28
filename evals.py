# import os
# import sys
# from pathlib import Path

# from openai import OpenAI

# from ragas import Dataset, experiment
# from ragas.llms import llm_factory
# from ragas.metrics import DiscreteMetric

# # Add the current directory to the path so we can import rag module when run as a script
# sys.path.insert(0, str(Path(__file__).parent))
# from rag import default_rag_client

# # openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# # rag_client = default_rag_client(llm_client=openai_client, logdir="evals/logs")
# # llm = llm_factory("gpt-4o", client=openai_client)


# # Create an OpenAI-compatible client for Ollama
# ollama_client = OpenAI(
#     api_key="ollama",  # Ollama doesn't require a real key
#     base_url="http://localhost:11434/v1"
# )
# rag_client = default_rag_client(llm_client=ollama_client, logdir="evals/logs")
# llm = llm_factory("llama3.2:latest", provider="openai", client=ollama_client)

# def load_dataset():
#     dataset = Dataset(
#         name="test_dataset",
#         backend="local/csv",
#         root_dir="evals",
#     )

#     data_samples = [
#         {
#             "question": "What is ragas 0.3",
#             "grading_notes": "- experimentation as the central pillar - provides abstraction for datasets, experiments and metrics - supports evals for RAG, LLM workflows and Agents",
#         },
#         {
#             "question": "how are experiment results stored in ragas 0.3?",
#             "grading_notes": "- configured using different backends like local, gdrive, etc - stored under experiments/ folder in the backend storage",
#         },
#         {
#             "question": "What metrics are supported in ragas 0.3?",
#             "grading_notes": "- provides abstraction for discrete, numerical and ranking metrics",
#         },
#     ]

#     for sample in data_samples:
#         row = {"question": sample["question"], "grading_notes": sample["grading_notes"]}
#         dataset.append(row)

#     # make sure to save it
#     dataset.save()
#     return dataset


# my_metric = DiscreteMetric(
#     name="correctness",
#     prompt="Check if the response contains points mentioned from the grading notes and return 'pass' or 'fail'.\nResponse: {response} Grading Notes: {grading_notes}",
#     allowed_values=["pass", "fail"],
# )


# @experiment()
# async def run_experiment(row):
#     response = rag_client.query(row["question"])

#     score = my_metric.score(
#         llm=llm,
#         response=response.get("answer", " "),
#         grading_notes=row["grading_notes"],
#     )

#     experiment_view = {
#         **row,
#         "response": response.get("answer", ""),
#         "score": score.value,
#         "log_file": response.get("logs", " "),
#     }
#     return experiment_view


# async def main():
#     dataset = load_dataset()
#     print("dataset loaded successfully", dataset)
#     experiment_results = await run_experiment.arun(dataset)
#     print("Experiment completed successfully!")
#     print("Experiment results:", experiment_results)

#     # Save experiment results to CSV
#     experiment_results.save()
#     csv_path = Path(".") / "experiments" / f"{experiment_results.name}.csv"
#     print(f"\nExperiment results saved to: {csv_path.resolve()}")


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(main())
import asyncio
import os
import sys
from pathlib import Path

from openai import OpenAI

from ragas import Dataset, experiment
from ragas.llms import llm_factory
from ragas.metrics import DiscreteMetric

# Make `rag` importable when this file is run as a script from any directory
sys.path.insert(0, str(Path(__file__).parent))
from rag import default_rag_client  # noqa: E402

# ----------------------------------------------------------------------------
# Configuration (override with environment variables)
# ----------------------------------------------------------------------------
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
RAG_MODEL = os.environ.get("RAG_MODEL", "llama3.2:latest")  # generator
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", RAG_MODEL)  # LLM-as-judge; use a bigger model if you can
EVALS_DIR = Path(__file__).parent / "evals"

# Ollama exposes an OpenAI-compatible API; the api_key just has to be non-empty.
ollama_client = OpenAI(api_key="ollama", base_url=OLLAMA_BASE_URL)

rag_client = default_rag_client(
    llm_client=ollama_client,
    logdir=str(EVALS_DIR / "logs"),
    model=RAG_MODEL,
    temperature=0.0,
)
judge_llm = llm_factory(JUDGE_MODEL, provider="openai", client=ollama_client)

# ----------------------------------------------------------------------------
# Dataset
# ----------------------------------------------------------------------------
DATA_SAMPLES = [
    {
        "question": "What is ragas 0.3",
        "grading_notes": "- experimentation as the central pillar - provides abstraction for datasets, experiments and metrics - supports evals for RAG, LLM workflows and Agents",
    },
    {
        "question": "how are experiment results stored in ragas 0.3?",
        "grading_notes": "- configured using different backends like local, gdrive, etc - stored under experiments/ folder in the backend storage",
    },
    {
        "question": "What metrics are supported in ragas 0.3?",
        "grading_notes": "- provides abstraction for discrete, numerical and ranking metrics",
    },
]


def load_dataset() -> Dataset:
    EVALS_DIR.mkdir(parents=True, exist_ok=True)
    dataset = Dataset(name="test_dataset", backend="local/csv", root_dir=str(EVALS_DIR))

    # Only seed the dataset once, otherwise every run appends duplicate rows.
    if len(dataset) == 0:
        for sample in DATA_SAMPLES:
            dataset.append(
                {"question": sample["question"], "grading_notes": sample["grading_notes"]}
            )
        dataset.save()
    return dataset


# ----------------------------------------------------------------------------
# Metric
# ----------------------------------------------------------------------------
correctness_metric = DiscreteMetric(
    name="correctness",
    prompt=(
        "Check if the response contains points mentioned from the grading notes "
        "and return 'pass' or 'fail'.\n"
        "Response: {response} Grading Notes: {grading_notes}"
    ),
    allowed_values=["pass", "fail"],
)


# ----------------------------------------------------------------------------
# Experiment
# ----------------------------------------------------------------------------
@experiment()
async def run_experiment(row):
    # rag_client.query is synchronous; run it in a thread so rows don't block the event loop.
    result = await asyncio.to_thread(rag_client.query, row["question"])

    if result.get("error"):
        # The RAG call itself failed (e.g. Ollama down, model not pulled): don't ask
        # the judge to grade an error message.
        score_value = "fail"
    else:
        # `score` is the sync API, which matches the sync OpenAI client used above.
        score = correctness_metric.score(
            llm=judge_llm,
            response=result["answer"],
            grading_notes=row["grading_notes"],
        )
        score_value = score.value

    return {
        **row,
        "response": result["answer"],
        "score": score_value,
        "error": result.get("error") or "",
        "log_file": result.get("logs", ""),
    }


async def main():
    dataset = load_dataset()
    print("Dataset loaded:", dataset)

    results = await run_experiment.arun(dataset)
    results.save()
    print("Experiment completed. Results:", results)


if __name__ == "__main__":
    asyncio.run(main())