# NoLess Library 🚀

NoLess is a Python library for building complete machine-learning projects with the help of cooperative AI agents and local LLMs. It exposes the same generators, planners, and feedback loops that power the original CLI so you can embed them inside notebooks, services, or custom tooling.

## Why NoLess

- 🤖 **Multi-agent automation** – orchestrate dataset discovery, architecture design, and code generation with reusable agents.
- 🧱 **LLM-powered builders** – generate configs, models, training loops, and tests with a single call to `ModelGenerator`.
- 🔍 **Unified dataset search** – query OpenML, Hugging Face, Kaggle, and UCI from the `DatasetSearcher` API.
- 🛠️ **Interactive refinement** – use `InteractiveFeedbackLoop` to iteratively review and improve generated code.
- ✅ **Production-ready outputs** – every project ships with config, model, training, tests, requirements, and README files.

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/noless.git
cd noless

# Install dependencies
pip install -r requirements.txt

# Install the library in editable mode
pip install -e .
```

Optional extras:
- Install [Ollama](https://ollama.com) and pull at least one model (e.g. `ollama pull deepseek-r1:1.5b`).
- Configure Kaggle or Hugging Face credentials if you plan to download datasets automatically.

## Quick Start

```python
from noless.generator import ModelGenerator
from noless.ollama_client import OllamaClient

client = OllamaClient()
generator = ModelGenerator(llm_model="deepseek-r1:1.5b", ollama_client=client)
project = generator.create_project(
    task="image-classification",
    framework="pytorch",
    dataset="mnist",
    output_dir="./mnist_classifier",
)

print(project["files"])
```

The output directory now contains `config.yaml`, `model.py`, `train.py`, `test_model.py`, `requirements.txt`, and a README ready for version control.

## Key Modules

### `noless.generator.ModelGenerator`
Builds end-to-end ML project skeletons. Supports PyTorch, TensorFlow, and scikit-learn targets, optional Ollama-powered authoring, and automatic AI reviews via `CodeValidator`.

### `noless.autopilot.AutopilotPlanner`
Uses an LLM to interpret natural-language goals, ask clarifying questions, and produce structured blueprints (task, framework, dataset hints, architecture recommendations).

### `noless.search.DatasetSearcher`
Aggregates dataset discovery across OpenML, Hugging Face, Kaggle, and UCI. Returns normalized metadata and can download ready-to-use files.

### `noless.feedback_loop.InteractiveFeedbackLoop`
Provides a conversational refinement loop for any generated file. Supply code plus context and iteratively apply user or AI feedback.

### `noless.code_validator.CodeValidator`
Runs AI reviews against generated code using a larger reviewer model when available, returning improved code plus issue/suggestion lists.

### `noless.agents.MultiAgentSystem`
Optional cooperative layer that lets you run the six specialized agents (orchestrator, dataset, model, code, training, optimization) inside your own applications.

## End-to-End Pipeline Example

```python
from noless.autopilot import AutopilotPlanner
from noless.generator import ModelGenerator
from noless.search import DatasetSearcher
from noless.ollama_client import OllamaClient

client = OllamaClient()
planner = AutopilotPlanner(client, llm_model="deepseek-r1:1.5b")
analysis = planner.plan_project("detect defects in solar panel images")

searcher = DatasetSearcher()
datasets = searcher.search(analysis.dataset_query, limit=5)

project = ModelGenerator(
    llm_model="deepseek-r1:1.5b",
    reviewer_model="mixtral:8x7b",
    ollama_client=client,
).create_project(
    task=analysis.task,
    framework=analysis.framework,
    dataset=datasets[0].name if datasets else None,
    output_dir="./solar_inspector",
    dataset_metadata=datasets[0].__dict__ if datasets else None,
)
```

## Testing

Run the unit test suite after making changes:

```bash
python -m unittest
```

## License

NoLess is released under the MIT License. See `LICENSE` for details.
