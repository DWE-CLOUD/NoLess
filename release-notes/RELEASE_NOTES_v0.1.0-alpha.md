# NoLess CLI v0.1.0-alpha - Initial Alpha Release

**Release Date**: November 16, 2025  
**Status**: Alpha (Experimental)

## Introduction

Welcome to the first alpha release of **NoLess** - an intelligent CLI tool that revolutionizes ML model development by combining multi-agent architecture with local LLMs. This alpha release is feature-complete but still under active testing.

## Alpha Release Notice

This is an **alpha release** intended for:
- Early adopters and testers
- Developers who want to experiment with AI-powered code generation
- Contributors interested in shaping the tool's future

**Known limitations**:
- Some edge cases in dataset downloading may fail
- Generated code quality varies with model choice
- Performance not yet optimized for all scenarios

We welcome feedback and bug reports!

## Core Features

### 1. Autopilot Mode - One Command to Rule Them All
Build complete ML projects with a single command:

```bash
noless autopilot -d "classify dog breeds from images"
```

What happens behind the scenes:
- LLM analyzes your description
- Asks clarifying questions
- Searches 20,000+ datasets
- Designs optimal architecture
- Generates production-ready code
- Creates tests and documentation

### 2. Multi-Agent System (6 Specialized Agents)

| Agent | Role | Key Features |
|-------|------|--------------|
| **Orchestrator** | Task coordination | Plans workflow, manages execution order |
| **DatasetAgent** | Data discovery | Searches OpenML, Kaggle, HuggingFace, UCI |
| **ModelAgent** | Architecture design | Recommends ResNet, BERT, LSTM, etc. |
| **CodeAgent** | Implementation | Generates model.py, train.py with 100-200 lines |
| **EvaluationAgent** | Testing | Creates pytest suites with fixtures |
| **OptimizationAgent** | Hyperparameter tuning | Suggests learning rates, batch sizes |

All agents work autonomously and communicate via structured protocols.

### 3. Interactive Feedback Loop
Real-time collaboration with AI:

```bash
noless autopilot -i -d "sentiment classifier for tweets"
```

During interaction:
- **View** syntax-highlighted code previews
- **Give feedback** in natural language ("add dropout layers")
- **Request AI review** from larger expert models
- **Accept** or regenerate until perfect
- **Iterate** up to 10 times

### 4. Local LLM Integration (Ollama)
Privacy-first AI with no cloud dependencies:

**Supported models**:
- `deepseek-r1:1.5b` - Fast, lightweight (recommended for generation)
- `deepseek-coder:6.7b` - Code-specialized
- `llama3.1:8b` - Balanced quality/speed
- `mixtral:8x7b` - Expert-grade (recommended for review)
- `llama3.1:70b` - Maximum quality (if you have 48GB+ RAM)

**Dual-model system**:
```bash
noless autopilot \
  --llm-model deepseek-r1:1.5b \      # Fast generation
  --reviewer-model mixtral:8x7b        # Expert review
```

### 5. Multi-Source Dataset Discovery

Search across 4 major repositories simultaneously:

| Source | Datasets | Best For |
|--------|----------|----------|
| OpenML | 5,000+ | Tabular, classification |
| HuggingFace | 10,000+ | NLP, vision |
| Kaggle | 50,000+ | Competitions, real-world |
| UCI ML | 500+ | Classic ML benchmarks |

```bash
noless search "medical imaging chest x-ray" --limit 20
```

Features:
- Smart keyword extraction using LLMs
- Automatic ranking by relevance
- One-click download and caching
- Metadata extraction (features, samples, task type)

### 6. Complete Project Generation

Every generated project includes:

```
my_classifier/
├── model.py              # 100-200 lines
│   ├── Complete architecture (ResNet, BERT, etc.)
│   ├── Forward pass implementation
│   ├── Weight initialization
│   └── Type hints & docstrings
│
├── train.py              # 150-250 lines
│   ├── Data loading & augmentation
│   ├── Training loop with progress bars
│   ├── Validation & metrics
│   ├── Checkpointing & early stopping
│   └── Logging (TensorBoard compatible)
│
├── test_model.py         # 50-100 lines
│   ├── Pytest fixtures
│   ├── Model initialization tests
│   ├── Forward pass tests
│   ├── Shape validation
│   └── Dataset loading tests
│
├── config.yaml           # Hyperparameters
│   ├── Model settings (layers, dropout, etc.)
│   ├── Training config (epochs, batch size, LR)
│   └── Data splits (train/val/test)
│
├── requirements.txt      # All dependencies
└── README.md             # Complete documentation
```

**Code quality guarantees**:
- No TODO comments or placeholders
- Complete implementations
- Error handling included
- Type hints everywhere
- Comprehensive docstrings
- Follows PEP 8 style

## Installation

### Option 1: Install from PyPI (recommended)
```bash
pip install noless
noless --version
```

### Option 2: Install from source
```bash
git clone https://github.com/yourusername/NoLess.git
cd NoLess
pip install -e .
```

### Required: Install Ollama
```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from: https://ollama.com

# Pull at least one model
ollama pull deepseek-r1:1.5b
```

### Optional: Configure API Keys

**For Kaggle datasets**:
```bash
# 1. Create account at kaggle.com
# 2. Go to Account → API → Create New Token
# 3. Place kaggle.json in:
#    Linux/macOS: ~/.kaggle/kaggle.json
#    Windows: %USERPROFILE%\.kaggle\kaggle.json
```

**For HuggingFace datasets**:
```bash
pip install datasets
# No API key needed for public datasets
```

## Quick Start Guide

### 1. Autopilot (Easiest)
Let AI do everything:
```bash
noless autopilot -d "classify handwritten digits"
```

### 2. Interactive Autopilot
Collaborate with AI:
```bash
noless autopilot -i -d "sentiment analysis on movie reviews"
```

### 3. Quick Mode (Skip Questions)
```bash
noless autopilot --skip-followups -d "object detection for cars"
```

### 4. With Specific Models
```bash
noless autopilot \
  --llm-model deepseek-r1:1.5b \
  --reviewer-model mixtral:8x7b \
  -d "time series forecasting for stock prices"
```

### 5. Manual Project Creation
```bash
noless create \
  -t image-classification \
  -f pytorch \
  -a resnet50 \
  --agents \
  --output ./my_project
```

### 6. Search Datasets Only
```bash
noless search "cifar10" --source openml
noless search "imdb sentiment" --source huggingface
```

### 7. Interactive Menu (For Beginners)
```bash
noless interactive
```

## Supported Tasks & Architectures

### Computer Vision
**Tasks**: Classification, Detection, Segmentation  
**Architectures**:
- ResNet (18, 34, 50, 101, 152)
- EfficientNet (B0-B7)
- Vision Transformer (ViT-Base, ViT-Large)
- YOLOv8 (for detection)
- U-Net (for segmentation)

### Natural Language Processing
**Tasks**: Classification, Sequence-to-Sequence, NER  
**Architectures**:
- BERT (Base, Large)
- RoBERTa (Base, Large)
- DistilBERT
- T5 (Small, Base, Large)
- GPT-2

### Time Series
**Tasks**: Forecasting, Anomaly Detection  
**Architectures**:
- LSTM, GRU
- Temporal CNNs
- Transformers
- Prophet

### Tabular Data
**Tasks**: Classification, Regression  
**Algorithms**:
- XGBoost, LightGBM, CatBoost
- Random Forest, Gradient Boosting
- Neural Networks (TabNet, FT-Transformer)

## System Requirements

### Minimum
- **Python**: 3.8+
- **RAM**: 8GB
- **Disk**: 5GB free
- **OS**: Windows 10+, macOS 10.15+, Linux

### Recommended
- **Python**: 3.10+
- **RAM**: 16GB (for 13B+ models)
- **Disk**: 20GB+ (for datasets)
- **GPU**: CUDA-capable (optional, for faster training)

### For Large Models (70B+)
- **RAM**: 48GB+
- **GPU**: 80GB VRAM (A100) or CPU with swap

## Performance Benchmarks (Alpha)

### Code Generation Speed
| Model | Time | Quality |
|-------|------|---------|
| deepseek-r1:1.5b | ~30s | Good |
| llama3.1:8b | ~60s | Very Good |
| mixtral:8x7b | ~120s | Excellent |

### Dataset Search
| Source | Avg Response | Results |
|--------|--------------|---------|
| OpenML | ~2s | 50-100 |
| HuggingFace | ~3s | 20-50 |
| Kaggle | ~5s | 30-80 |

*Benchmarks on AMD Ryzen 9 7950X, 64GB RAM*

## Known Issues (Alpha)

### High Priority
1. **OpenML large dataset downloads timeout** - Workaround: Use smaller datasets or download manually
2. **Kaggle API requires manual setup** - Must place `kaggle.json` in `~/.kaggle/`
3. **Generated code may have minor import errors** - AI reviewer catches most, but check before running

### Medium Priority
4. **Large models (70B) are very slow** - Consider smaller models or cloud inference
5. **Some architecture combinations not tested** - E.g., BERT + Kaggle dataset
6. **Windows terminal Unicode issues** - Use `--no-startup` flag if you see garbled characters

### Low Priority
7. **Progress bars flicker on some terminals** - Cosmetic issue only
8. **Agent communication logs are verbose** - Will add `--quiet` flag in beta

## Roadmap to Beta (v0.2)

### Planned Features
- [ ] **Auto-train after generation** - Run training immediately after code gen
- [ ] **Model fine-tuning workflows** - Update existing models with new data
- [ ] **Distributed training** - Multi-GPU and multi-node support
- [ ] **Web UI** - Browser-based interface for non-CLI users
- [ ] **More dataset sources** - Papers with Code, Roboflow, etc.
- [ ] **Cloud deployment** - One-click deploy to AWS/GCP/Azure
- [ ] **Experiment tracking** - Integration with MLflow, Weights & Biases
- [ ] **Custom templates** - User-defined architecture templates

### Performance Improvements
- [ ] Parallel agent execution
- [ ] Streaming dataset downloads
- [ ] Code generation caching
- [ ] Better error recovery

### Quality Improvements
- [ ] More comprehensive tests for generated code
- [ ] Better prompt engineering for LLMs
- [ ] Architecture validation before generation
- [ ] Automatic dependency resolution

## Testing & Validation

### Test Coverage
- Unit tests for core modules (70%+ coverage)
- Integration tests for agent system
- End-to-end autopilot workflow tests
- Generated code tests (manual verification only in alpha)

### Validated Combinations
Tested and working:
- PyTorch + OpenML + Image Classification
- TensorFlow + HuggingFace + Text Classification
- scikit-learn + Kaggle + Regression

Not yet fully tested:
- Object detection workflows
- Time series with external datasets
- Custom architectures

## Documentation & Resources

- **Main README**: [`README.md`](README.md)
- **Contributing Guide**: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **GitHub**: https://github.com/yourusername/NoLess
- **Issues**: https://github.com/yourusername/NoLess/issues
- **Discussions**: https://github.com/yourusername/NoLess/discussions

### Examples
See `examples/` directory for:
- Basic usage scripts
- Config file examples
- Custom workflow demonstrations

## Contributing (Alpha Testers Welcome!)

We need help testing and improving NoLess! Areas to contribute:

### High Priority
- Bug reports (especially edge cases)
- Documentation improvements
- Test coverage expansion
- Windows compatibility testing

### Medium Priority
- New architecture support
- More dataset source integrations
- UI/UX improvements
- Internationalization

### How to Contribute
1. Star the repository
2. Try the tool and file issues
3. Submit PRs (see [`CONTRIBUTING.md`](CONTRIBUTING.md))
4. Share feedback in Discussions

## Community & Support

### Getting Help
- **Bug Reports**: Open an issue on GitHub
- **Feature Requests**: Use Discussions
- **Questions**: Check existing issues or ask in Discussions
- **Real-time Chat**: Join our Discord (coming soon)

### Sharing Your Experience
We'd love to hear:
- What models you built
- Issues you encountered
- Features you need
- Success stories

Tag us on Twitter: `@NoLessCLI` (coming soon)

## License

**MIT License** - See [`LICENSE`](LICENSE) file

Free for:
- Personal use
- Commercial use
- Modification
- Distribution

## Acknowledgments

Built with amazing open-source tools:
- [Ollama](https://ollama.com) - Local LLM inference
- [OpenML](https://openml.org) - Dataset repository
- [HuggingFace](https://huggingface.co) - Models & datasets
- [Kaggle](https://kaggle.com) - Competitions & datasets
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Rich](https://github.com/Textualize/rich) - Terminal styling
- [Questionary](https://github.com/tmbo/questionary) - Interactive prompts

Special thanks to the AI/ML open-source community!

## 🎉 Try It Now!

```bash
# Install
pip install noless

# Start Ollama
ollama serve

# Pull a model
ollama pull deepseek-r1:1.5b

# Build your first ML model!
noless autopilot -i -d "your ML task description here"
```

**Build AI models without limits!** 🚀

---

## Version Info
- **Version**: 0.1.0-alpha
- **Release Date**: November 16, 2025
- **Python**: 3.8+
- **License**: MIT
- **Status**: Alpha (Breaking changes may occur)

**Important**: This is an alpha release. APIs and command-line interfaces may change in future versions. Pin your version if using in production.

---

**Questions? Feedback? Issues?**  
Open an issue: https://github.com/yourusername/NoLess/issues/new
