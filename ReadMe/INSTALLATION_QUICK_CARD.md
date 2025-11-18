# NoLess Installation Quick Card

## One-Line Installation Commands

### Minimal (5 MB)
```bash
pip install noless
```

### Light (15 MB) - APIs only
```bash
pip install noless[light]
```

### Standard (50 MB) - Datasets + APIs
```bash
pip install "noless[datasets,apis]"
```

### ML Ready (400 MB) - Deep Learning
```bash
pip install "noless[ml,data,datasets,apis]"
```

### Full (800+ MB) - Everything
```bash
pip install "noless[all]"
```

### Development (1+ GB) - Contributing
```bash
pip install "noless[all,dev]"
```

---

## Quick Reference Table

| Need | Command | Size |
|------|---------|------|
| **Test/Learn** | `pip install noless` | 5 MB |
| **Local LLMs** | `pip install noless` | 5 MB |
| **LLM APIs** | `pip install noless[light]` | 15 MB |
| **Datasets** | `pip install noless[datasets]` | 50 MB |
| **Data Science** | `pip install noless[data]` | 100 MB |
| **Full ML** | `pip install noless[ml,data,datasets]` | 400 MB |
| **Everything** | `pip install noless[all]` | 800+ MB |
| **Dev/Contrib** | `pip install noless[all,dev]` | 1+ GB |

---

## Feature Breakdown

### 📦 Core (Always Included)
- ✅ CLI functionality
- ✅ Code review & generation
- ✅ Refinement mode
- ✅ Local LLM support
- ✅ HTML parsing
- **5 MB**

### 🤖 ML Frameworks [ml]
- ✅ PyTorch
- ✅ TensorFlow
- ✅ Scikit-learn
- **1.5 GB**

### 📊 Data Processing [data]
- ✅ Pandas
- ✅ NumPy
- **150 MB**

### 📚 Datasets [datasets]
- ✅ Kaggle API
- ✅ HuggingFace Hub
- ✅ OpenML
- **100 MB**

### 🧠 LLM APIs [apis]
- ✅ OpenAI
- ✅ Anthropic
- **10 MB**

### 🎨 UI [ui]
- ✅ Interactive prompts
- ✅ Colored output
- ✅ ASCII art
- **5 MB**

### 🔍 Analysis [analysis]
- ✅ Bandit (security)
- ✅ Radon (metrics)
- **20 MB**

### 🛠️ Development [dev]
- ✅ Pytest
- ✅ Black
- ✅ Flake8
- ✅ MyPy
- **200 MB**

---

## Installation Scenarios

### Scenario 1: I Just Want to Learn
```bash
pip install noless
# 5 MB, takes 10 seconds
# Test with: noless --version
```

### Scenario 2: I Use OpenAI/Anthropic
```bash
pip install "noless[light]"
# 15 MB, includes API support
# Test with: noless --version
```

### Scenario 3: I Work with Datasets
```bash
pip install "noless[datasets,apis,ui]"
# 60 MB, full dataset and API support
```

### Scenario 4: I'm a Data Scientist
```bash
pip install "noless[ml,data,datasets]"
# 400 MB, PyTorch/TensorFlow included
```

### Scenario 5: I'm Contributing to NoLess
```bash
pip install "noless[all,dev]"
# 1+ GB, everything for development
```

---

## Size Comparison at a Glance

```
pip install noless
├─ 5 MB ..................... Minimal
└─ Fast: 10 seconds

pip install noless[light]
├─ 15 MB .................... Light
└─ Fast: 15 seconds

pip install "noless[datasets,apis]"
├─ 50 MB .................... Standard
└─ Medium: 30 seconds

pip install "noless[ml,data,datasets]"
├─ 400 MB ................... ML Setup
└─ Slow: 2 minutes

pip install noless[all]
├─ 800+ MB .................. Full
└─ Very slow: 5 minutes
```

---

## Add Features Later

Start minimal, add features when you need them:

```bash
# Start with minimal
pip install noless

# Later, add ML frameworks
pip install "noless[ml]"

# Or add datasets
pip install "noless[datasets]"

# Or add both
pip install "noless[ml,datasets]"
```

---

## Check Installation

```bash
# Verify it's installed
noless --version

# Run tests
python -c "import noless; print('✓ Installed')"

# Check what was installed
pip show noless
```

---

## Common Installation Errors

| Error | Solution |
|-------|----------|
| "Module not found: torch" | `pip install noless[ml]` |
| "Module not found: pandas" | `pip install noless[data]` |
| "Module not found: kaggle" | `pip install noless[datasets]` |
| "Module not found: openai" | `pip install noless[light]` or `noless[apis]` |
| Package too large | Start with `pip install noless` (5 MB) |

---

## Uninstall & Reinstall with Different Size

```bash
# If you installed [all] but want just [light]
pip uninstall noless
pip install noless[light]
# Saves 700+ MB!
```

---

## Pre-built Installation Commands

Copy-paste these based on your needs:

**Beginner/Tester**
```
pip install noless
```

**Local LLM User**
```
pip install noless
```

**API Integration**
```
pip install "noless[light]"
```

**Dataset Work**
```
pip install "noless[datasets,apis,ui]"
```

**ML Engineer**
```
pip install "noless[ml,data,datasets,apis,ui]"
```

**Full Power User**
```
pip install "noless[all]"
```

**Developer/Contributor**
```
pip install "noless[all,dev]"
```

---

## About the Optimization

**Old way:** 1.4 GB required, everything installed
**New way:** 5 MB minimal, add what you need
**Result:** 280x smaller base install

---

## Documentation

For detailed information, see:
- **LIGHTWEIGHT_INSTALLATION.md** - Full guide
- **PACKAGE_OPTIMIZATION_SUMMARY.md** - Technical details
- **README.md** - General information

---

## Support

Questions about installation?
1. Check the error message
2. Look up in "Common Installation Errors" above
3. See LIGHTWEIGHT_INSTALLATION.md for full guide
4. File an issue if stuck

---

**Choose your size. Install what you need. Enjoy NoLess! 🚀**
