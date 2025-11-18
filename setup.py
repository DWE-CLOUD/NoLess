from pathlib import Path
from setuptools import setup, find_packages

README_PATH = Path(__file__).parent / "README.md"

BASE_REQUIREMENTS = [
    "click>=8.1.0",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "jinja2>=3.1.0",
    "openml>=0.14.0",
    "questionary>=2.0.0",
    "prompt_toolkit>=3.0.0",
    "colorama>=0.4.6",
    "pyfiglet>=1.0.0",
]

ML_REQUIREMENTS = [
    "torch>=2.0.0",
    "tensorflow>=2.13.0",
    "scikit-learn>=1.3.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
]

DATA_REQUIREMENTS = [
    "huggingface-hub>=0.19.0",
    "kaggle>=1.5.16",
]

LLM_REQUIREMENTS = [
    "anthropic>=0.39.0",
    "openai>=1.0.0",
]

ALL_EXTRAS = sorted({
    *ML_REQUIREMENTS,
    *DATA_REQUIREMENTS,
    *LLM_REQUIREMENTS,
})

setup(
    name="noless",
    version="0.2.1a2",
    author="NoLess Team",
    description="Multi-agent CLI for automatic dataset discovery and ML project generation",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/DWE-CLOUD/NoLess",
    project_urls={
        "Source": "https://github.com/DWE-CLOUD/NoLess",
        "Issues": "https://github.com/DWE-CLOUD/NoLess/issues",
        "Documentation": "https://github.com/DWE-CLOUD/NoLess#readme",
    },
    license="MIT",
    packages=find_packages(exclude=("tests", "tests.*", "examples", "examples.*")),
    include_package_data=True,
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
    ],
    keywords="cli ai machine-learning autopilot multi-agent",
    python_requires=">=3.8",
    install_requires=BASE_REQUIREMENTS,
    extras_require={
        "ml": ML_REQUIREMENTS,
        "data": DATA_REQUIREMENTS,
        "llm": LLM_REQUIREMENTS,
        "all": ALL_EXTRAS,
    },
    entry_points={
        "console_scripts": [
            "noless=noless.cli:main",
        ],
    },
)
