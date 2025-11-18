# NoLess Lightweight Installation Guide

**Current Package Size:** ~5-8 MB (core only)
**With All Features:** ~800 MB+ (includes ML frameworks)

NoLess v0.2.1a1 uses a **modular dependency system** - install only what you need!

---

## Quick Installation Options

### ⚡ Minimal Installation (5 MB)
Perfect for CLI-only usage or testing:
```bash
pip install noless
```

**Includes:**
- ✅ Core CLI functionality
- ✅ Local LLM support (Ollama)
- ✅ Code review and generation
- ✅ Refinement mode
- ✅ Basic HTML parsing

**Does NOT include:**
- ❌ ML frameworks (torch, tensorflow)
- ❌ Data processing (pandas, numpy)
- ❌ Dataset APIs (Kaggle, HuggingFace)
- ❌ Advanced UI enhancements

**Perfect for:** Testing, learning, basic code review

---

### 🚀 Standard Installation (50 MB)
With dataset support and APIs:
```bash
pip install noless[datasets,apis]
```

**Adds:**
- ✅ Kaggle API support
- ✅ HuggingFace Hub integration
- ✅ OpenML dataset access
- ✅ OpenAI/Anthropic API support
- ✅ Advanced UI features

**Great for:** Working with datasets, using LLM APIs

---

### 🔬 ML Scientist Installation (400 MB)
With ML frameworks:
```bash
pip install noless[ml,data,datasets,apis]
```

**Adds:**
- ✅ PyTorch deep learning
- ✅ TensorFlow support
- ✅ Scikit-learn ML algorithms
- ✅ Pandas data processing
- ✅ NumPy scientific computing
- ✅ All dataset APIs

**Perfect for:** ML development, model training

---

### 🧪 Development Installation (1.2 GB)
Everything including dev tools:
```bash
pip install noless[all]
```

**Includes:**
- ✅ All ML frameworks
- ✅ All datasets and APIs
- ✅ Code analysis tools (bandit, radon)
- ✅ Testing frameworks (pytest)
- ✅ Code formatters (black, flake8)
- ✅ Type checking (mypy)

**Perfect for:** Contributing, development

---

### 📦 Full Installation (Alias)
```bash
pip install noless[full]
# Same as: pip install noless[all]
```

---

## Modular Feature Installation

Install specific features as needed:

### ML Frameworks Only
```bash
pip install noless[ml]
# Installs: torch, tensorflow, scikit-learn
# Size: ~1.5 GB
```

### Data Processing Only
```bash
pip install noless[data]
# Installs: pandas, numpy
# Size: ~100 MB
```

### Dataset APIs Only
```bash
pip install noless[datasets]
# Installs: kaggle, huggingface-hub, openml
# Size: ~50 MB
```

### LLM APIs Only
```bash
pip install noless[apis]
# Installs: anthropic, openai
# Size: ~10 MB
```

### Code Analysis Tools
```bash
pip install noless[analysis]
# Installs: bandit, radon
# Size: ~20 MB
```

### UI Enhancements
```bash
pip install noless[ui]
# Installs: questionary, prompt-toolkit, colorama, pyfiglet
# Size: ~5 MB
```

### Development Tools
```bash
pip install noless[dev]
# Installs: pytest, black, flake8, mypy
# Size: ~200 MB
```

---

## Size Comparison

| Installation | Size | Install Time | Use Case |
|--------------|------|--------------|----------|
| **Minimal** | 5 MB | 10 sec | Learning, testing |
| **Light** | 15 MB | 15 sec | Basic usage with APIs |
| **Standard** | 50 MB | 30 sec | Dataset work |
| **ML** | 400 MB | 2 min | ML development |
| **Full** | 800+ MB | 5 min | Contribution |

---

## Installation Recommendations

### For Using with Local LLMs (Ollama)
```bash
pip install noless
# You're done! Use with ollama run model-name
```

### For Dataset Discovery
```bash
pip install noless[datasets]
# Access Kaggle, HuggingFace, OpenML datasets
```

### For LLM API Integration
```bash
pip install noless[apis,ui]
# Use OpenAI/Anthropic APIs with enhanced CLI
```

### For ML Model Training
```bash
pip install noless[ml,data,datasets]
# Full ML and data processing support
```

### For Contributing to NoLess
```bash
pip install noless[all]
# Everything needed for development
```

---

## Core Dependencies (Always Installed)

These lightweight packages are always included:

```
click               - CLI framework
requests            - HTTP requests
beautifulsoup4      - HTML parsing
rich                - Terminal output
pydantic            - Data validation
aiohttp             - Async HTTP
aiofiles            - Async file operations
pyyaml              - YAML parsing
jinja2              - Template engine
```

**Total size: ~20 MB** - Very lightweight!

---

## Optional Dependencies (Choose What You Need)

### 🤖 ML Frameworks (ml extra)
```
torch               - Deep learning (700 MB)
tensorflow          - Deep learning (400 MB)
scikit-learn        - ML algorithms (50 MB)
```

### 📊 Data Processing (data extra)
```
pandas              - Data manipulation (100 MB)
numpy               - Numerical computing (50 MB)
```

### 📚 Dataset APIs (datasets extra)
```
huggingface-hub     - HuggingFace datasets
kaggle              - Kaggle datasets
openml              - OpenML datasets
```

### 🧠 LLM APIs (apis extra)
```
anthropic           - Claude API
openai              - GPT API
```

### 🎨 UI Enhancement (ui extra)
```
questionary         - Interactive prompts
prompt-toolkit      - Terminal UI
colorama            - Colored output
pyfiglet            - ASCII art
```

### 🔍 Code Analysis (analysis extra)
```
bandit              - Security scanning
radon               - Code metrics
```

### 🛠️ Development (dev extra)
```
pytest              - Testing
black               - Code formatting
flake8              - Linting
mypy                - Type checking
```

---

## Common Installation Patterns

### Use Case: Data Science Project
```bash
pip install noless[ml,data,datasets,ui]
# Everything for ML with datasets
# ~450 MB
```

### Use Case: Quick Code Review
```bash
pip install noless
# Minimal setup, just review code
# ~5 MB
```

### Use Case: API-Based Generation
```bash
pip install noless[apis,ui]
# Use with OpenAI/Anthropic
# ~30 MB
```

### Use Case: Contributing to NoLess
```bash
pip install noless[all]
# Full development environment
# ~800 MB
```

---

## Upgrading Existing Installation

### From Heavy v0.2.0
Old installations might have all dependencies. To clean up:

```bash
# Uninstall and reinstall with minimal set
pip uninstall noless
pip install noless  # Just the core (5 MB)

# Then add features as needed
pip install noless[datasets]  # If you need datasets
pip install noless[ml]        # If you need ML frameworks
```

---

## Installing Additional Features Later

You can add features anytime:

```bash
# Current: installed with noless
pip install noless[ml,data]    # Add ML frameworks
```

---

## Checking Installed Features

To see what's installed:

```bash
pip show noless
# Shows version and size
```

To list installed optional dependencies:

```bash
python -c "import noless; print(noless.get_installed_features())"
```

---

## Troubleshooting

### "Module not found" when using ML features
**Fix:** Install the feature: `pip install noless[ml]`

### Package size seems large
**Check:** Run `pip show noless` to see installed size
**Solution:** Uninstall and reinstall with specific extras

### Want to use all features
**Solution:** `pip install noless[all]`

---

## Building from Source (Lightest)

Clone and install in development mode with minimal deps:

```bash
git clone https://github.com/noless/noless.git
cd noless

# Install with core only
pip install -e .

# Or with features
pip install -e .[ml,datasets]
```

---

## Docker Usage (Recommended for Heavy Setup)

For users who need everything, use Docker to isolate dependencies:

```dockerfile
FROM python:3.11-slim

RUN pip install noless[all]

ENTRYPOINT ["noless"]
```

Build and run:
```bash
docker build -t noless:latest .
docker run --rm -v $(pwd):/workspace noless code-review model.py
```

---

## Package Files Excluded (to Keep it Light)

The following are excluded from the PyPI package:
- All test files (~2 MB)
- Documentation markdown files (~5 MB)
- Example projects (~10 MB)
- Build artifacts
- IDE configuration
- CI/CD configuration

This saves ~17 MB on the package download!

---

## Summary: Size by Installation Type

```
pip install noless
└── 5 MB - Core only

pip install noless[light]
└── 15 MB - Core + APIs

pip install noless[datasets,apis]
└── 50 MB - Core + Datasets + APIs

pip install noless[ml,data,datasets,apis]
└── 400 MB - Full ML setup

pip install noless[all]
└── 800+ MB - Everything
```

---

## FAQ

**Q: Can I install only PyTorch without TensorFlow?**
A: No, the `[ml]` extra includes both. But you can manually uninstall TensorFlow if you only need PyTorch.

**Q: Does core functionality work without ML frameworks?**
A: Yes! The core (5 MB) includes all essential features. ML frameworks are truly optional.

**Q: Can I switch from heavy to light installation?**
A: Yes! `pip uninstall noless && pip install noless` will give you minimal setup.

**Q: What if I need a feature later?**
A: Simply install the extras: `pip install noless[ml]` adds ML frameworks.

---

## Conclusion

NoLess is now **truly modular**:
- **Minimal:** 5 MB for core features
- **Flexible:** Add only what you need
- **Lightweight:** No forced dependencies
- **Scalable:** Grow as your needs grow

Choose your installation and enjoy! 🚀
