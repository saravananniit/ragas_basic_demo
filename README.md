<!-- Build a proper venv and pin langchain-community lower

powershell
mkdir ragas-ollama; cd ragas-ollama
uv venv
.venv\Scripts\activate
uv pip install ragas "langchain-community<0.3"
ragas quickstart rag_eval
cd rag_eval -->

# RAG Evaluation

Evaluate a RAG (Retrieval Augmented Generation) system with custom metrics

## Quick Start

### 1. Set Your API Key

Choose your LLM provider:

```bash
# OpenAI (default)
export OPENAI_API_KEY="your-openai-key"

# Or use Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-key"

# Or use Google Gemini
export GOOGLE_API_KEY="your-google-key"
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
pip install -e .
```

### 3. Run the Evaluation

Using `uv`:

```bash
uv run python evals.py
```

Or using `pip`:

```bash
python evals.py
```

## Project Structure

```
rag_eval/
├── README.md           # This file
├── pyproject.toml      # Project configuration
├── rag.py              # Your RAG application code
├── evals.py            # Evaluation workflow
├── __init__.py         # Makes this a Python package
└── evals/              # Evaluation-related data
    ├── datasets/       # Test datasets
    ├── experiments/    # Experiment results
    └── logs/           # Evaluation logs and traces
```

## Customization

### Modify the LLM Provider

In `evals.py`, update the LLM configuration:

```python
from ragas.llms import llm_factory

# Use Anthropic Claude
llm = llm_factory("claude-3-5-sonnet-20241022", provider="anthropic")

# Use Google Gemini
llm = llm_factory("gemini-1.5-pro", provider="google")

# Use local Ollama
llm = llm_factory("mistral", provider="ollama", base_url="http://localhost:11434")
```

### Customize Test Cases

Edit the `load_dataset()` function in `evals.py` to add or modify test cases.

### Change Evaluation Metrics

Update the `my_metric` definition in `evals.py` to use different grading criteria.

## Documentation

Visit https://docs.ragas.io for more information.


(ragas_demo) PS C:\Users\zadmin\Desktop\ragas_demo> ragas quickstart rag_eval
⠸ Creating documentation...

✓ Created RAG Evaluation project at: rag_eval

Next Steps:
  cd rag_eval
  uv sync
  export OPENAI_API_KEY='your-api-key'
  uv run python evals.py

📚 For detailed instructions, see:
  https://docs.ragas.io/en/latest/getstarted/quickstart/

uv run python -c "import pandas as pd, glob; f=glob.glob('evals/**/blissful_codd.csv', recursive=True)[0]; print(f); print(pd.read_csv(f)[['question','response','score','error']].to_string())"