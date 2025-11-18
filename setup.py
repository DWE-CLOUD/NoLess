from pathlib import Path
from setuptools import setup, find_packages

README_PATH = Path(__file__).parent / "README.md"

# Read version from __version__.py
version_file = Path(__file__).parent / "noless" / "__version__.py"
version_dict = {}
exec(version_file.read_text(), version_dict)
VERSION = version_dict.get("__version__", "0.2.1a1")

# Core dependencies - minimal, lightweight
CORE_REQUIRES = [
    "click>=8.1.0",                    # CLI framework
    "requests>=2.31.0",                # HTTP requests
    "beautifulsoup4>=4.12.0",          # HTML parsing
    "rich>=13.0.0",                    # Terminal output
    "pydantic>=2.0.0",                 # Data validation
    "aiohttp>=3.8.0",                  # Async HTTP
    "aiofiles>=23.1.0",                # Async file I/O
    "pyyaml>=6.0",                     # YAML parsing
    "jinja2>=3.1.0",                   # Template engine
]

# Optional dependencies organized by feature
EXTRAS = {
    # ML frameworks (heavy, optional)
    "ml": [
        "torch>=2.0.0",
        "tensorflow>=2.13.0",
        "scikit-learn>=1.3.0",
    ],

    # Data processing (heavy, optional)
    "data": [
        "pandas>=2.0.0",
        "numpy>=1.24.0",
    ],

    # Dataset platforms (medium, optional)
    "datasets": [
        "huggingface-hub>=0.19.0",
        "kaggle>=1.5.16",
        "openml>=0.14.0",
    ],

    # LLM APIs (light, optional)
    "apis": [
        "anthropic>=0.39.0",
        "openai>=1.0.0",
    ],

    # UI enhancements (light, optional)
    "ui": [
        "questionary>=2.0.0",
        "prompt_toolkit>=3.0.0",
        "colorama>=0.4.6",
        "pyfiglet>=1.0.0",
    ],

    # Code analysis (optional)
    "analysis": [
        "bandit>=1.7.4",
        "radon>=6.0.0",
    ],

    # Development and testing
    "dev": [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "mypy>=1.0.0",
    ],
}

# Convenience extras
EXTRAS["all"] = [dep for deps in EXTRAS.values() for dep in deps]
EXTRAS["full"] = EXTRAS["all"]
EXTRAS["light"] = EXTRAS.get("apis", [])  # Just APIs for light installation

setup(
    name="noless",
    version=VERSION,
    author="NoLess Team",
    description="AI-powered ML project generation with local LLMs - lightweight and modular",
    long_description=README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "",
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/NoLess",
    project_urls={
        "Source": "https://github.com/your-org/NoLess",
        "Issues": "https://github.com/your-org/NoLess/issues",
        "Documentation": "https://github.com/your-org/NoLess#readme",
    },
    license="MIT",
    packages=find_packages(
        exclude=(
            "tests", "tests.*",
            "examples", "examples.*",
            "docs", "docs.*",
            "*.egg-info", "dist", "build"
        )
    ),
    include_package_data=False,  # Don't include extra files
    package_data={
        "noless": ["py.typed"],  # Include type hints marker
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="cli ai machine-learning autopilot multi-agent llm",
    python_requires=">=3.8",
    install_requires=CORE_REQUIRES,
    extras_require=EXTRAS,
    entry_points={
        "console_scripts": [
            "noless=noless.cli:main",
        ],
    },
    zip_safe=False,
)
