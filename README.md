# NoLess CLI 🚀

NoLess is a multi-agent command-line assistant that searches datasets, plans model architectures, and generates production-ready ML projects with help from local LLMs (via Ollama). Install it with pip and launch the `noless` command to start building models in minutes.

## Installation

```bash
pip install noless
```

Requirements:
- Python 3.8 or newer
- pip (or uv/pipx) to install the package
- [Ollama](https://ollama.com) running locally for LLM-powered features (`ollama serve` plus at least one model such as `deepseek-r1:1.5b`)
- Optional dataset credentials (Kaggle API token, Hugging Face token) if you plan to download private datasets

### Install from source (development mode)

```bash
git clone https://github.com/your-org/NoLess.git
cd NoLess
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
pip install -r requirements.txt
pip install -e .
```

Run the test suite before publishing:

```bash
python -m unittest
```

## Quick Start (CLI)

```bash
# 1. Let autopilot do everything from a plain-language description
noless autopilot -d "classify dog breeds from photos"

# 2. Create a project with explicit task/framework settings
noless create -t image-classification -f pytorch --agents --output ./doggo_ai

# 3. Search for datasets across OpenML, Hugging Face, Kaggle, and UCI
noless search -q "sentiment analysis" --limit 15

# 4. Launch the guided interactive experience
noless interactive
```

Common flags:
- `--llm-model`, `--reviewer-model` to pick specific Ollama models
- `--skip-followups` to bypass clarifying questions in autopilot mode
- `--refine` or `-i/--interactive` to enable human-in-the-loop refinement

## Features

- 🤖 **Multi-agent orchestration** – six specialized agents (orchestrator, dataset, model, code, training, optimization) collaborate to deliver end-to-end projects.
- 🔍 **Unified dataset search** – aggregate OpenML, Kaggle, Hugging Face, and UCI metadata, then download the selected dataset automatically.
- ⚡ **LLM-powered generation** – produce `model.py`, `train.py`, `config.yaml`, `test_model.py`, and README files with validated code.
- 🧪 **AI reviewer** – optional larger reviewer model provides code critiques and improvements via `CodeValidator`.
- 💬 **Interactive feedback loop** – preview code, request edits, or accept the final result right from the terminal.

## CLI Command Overview

| Command | Purpose |
| --- | --- |
| `noless autopilot` | Describe your goal once; autopilot chooses datasets, plans architecture, and generates the project. |
| `noless create` | Manually specify task/framework/dataset while still leveraging agents and LLMs. |
| `noless search` | Find datasets across supported sources with optional AI ranking. |
| `noless interactive` | Guided UI for new users (menus for search, build, stats, templates). |
| `noless agents` | Inspect the six-agent network, capabilities, and status. |
| `noless analyze` | Analyze an existing project for structure and best practices. |
| `noless benchmark` | Benchmark models/datasets and export metric reports. |

Run `noless --help` or `noless <command> --help` for the full option set.

## Library Usage (Optional)

The CLI is built on importable modules. You can embed the same components inside notebooks or services:

```python
from noless.generator import ModelGenerator
from noless.ollama_client import OllamaClient

client = OllamaClient()
project = ModelGenerator(
    llm_model="deepseek-r1:1.5b",
    reviewer_model="mixtral:8x7b",
    ollama_client=client,
).create_project(
    task="image-classification",
    framework="pytorch",
    dataset="mnist",
    output_dir="./mnist_classifier",
)

print(project["files"])
```

## Publishing to PyPI

1. Bump the version in `noless/__init__.py` and `setup.py`.
2. Build source and wheel artifacts:
   ```bash
   python -m pip install --upgrade build twine
   python -m build
   ```
3. Inspect the files under `dist/` and upload them to PyPI (or TestPyPI):
   ```bash
   twine upload dist/*
   # or for TestPyPI
   twine upload --repository testpypi dist/*
   ```
4. Verify the published package:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple noless
   noless --help
   ```

## License

NoLess is released under the MIT License. See `LICENSE` for details.

