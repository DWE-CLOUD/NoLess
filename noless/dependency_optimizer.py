"""Lazy dependency loading and optimization."""

from typing import Optional, Dict, Any
import sys
from importlib import import_module
from functools import wraps


class DependencyOptimizer:
    """Manages lazy loading of optional dependencies."""

    OPTIONAL_DEPENDENCIES = {
        "torch": {
            "package": "torch",
            "frameworks": ["pytorch"],
            "required_for": "PyTorch-based models",
            "install_command": "pip install torch"
        },
        "tensorflow": {
            "package": "tensorflow",
            "frameworks": ["tensorflow", "keras"],
            "required_for": "TensorFlow/Keras-based models",
            "install_command": "pip install tensorflow"
        },
        "sklearn": {
            "package": "sklearn",
            "frameworks": ["scikit-learn"],
            "required_for": "Scikit-learn models",
            "install_command": "pip install scikit-learn"
        },
        "bandit": {
            "package": "bandit",
            "frameworks": [],
            "required_for": "Advanced security analysis",
            "install_command": "pip install bandit"
        },
        "radon": {
            "package": "radon",
            "frameworks": [],
            "required_for": "Complexity analysis",
            "install_command": "pip install radon"
        }
    }

    _loaded_modules: Dict[str, Any] = {}

    @classmethod
    def require_dependency(cls, dep_name: str) -> Any:
        """
        Load a dependency on demand.

        Args:
            dep_name: Name of dependency

        Returns:
            Imported module

        Raises:
            ImportError: If dependency is not available
        """
        # Check if already loaded
        if dep_name in cls._loaded_modules:
            return cls._loaded_modules[dep_name]

        # Check if dependency exists
        if dep_name not in cls.OPTIONAL_DEPENDENCIES:
            raise ValueError(f"Unknown dependency: {dep_name}")

        dep_info = cls.OPTIONAL_DEPENDENCIES[dep_name]
        package_name = dep_info["package"]

        try:
            # Try to import
            module = import_module(package_name)
            cls._loaded_modules[dep_name] = module
            return module
        except ImportError:
            raise ImportError(
                f"Required dependency '{dep_name}' is not installed.\n"
                f"Install it using: {dep_info['install_command']}\n"
                f"This is needed for: {dep_info['required_for']}"
            )

    @classmethod
    def has_dependency(cls, dep_name: str) -> bool:
        """
        Check if a dependency is available.

        Args:
            dep_name: Name of dependency

        Returns:
            True if available, False otherwise
        """
        try:
            cls.require_dependency(dep_name)
            return True
        except ImportError:
            return False

    @classmethod
    def get_available_frameworks(cls) -> list:
        """
        Get list of available ML frameworks.

        Returns:
            List of framework names
        """
        available = []
        for dep_name, dep_info in cls.OPTIONAL_DEPENDENCIES.items():
            if dep_info["frameworks"] and cls.has_dependency(dep_name):
                available.extend(dep_info["frameworks"])
        return list(set(available))

    @classmethod
    def get_missing_dependencies(cls) -> Dict[str, Dict[str, str]]:
        """
        Get list of missing optional dependencies.

        Returns:
            Dictionary of missing dependencies and install commands
        """
        missing = {}
        for dep_name, dep_info in cls.OPTIONAL_DEPENDENCIES.items():
            if not cls.has_dependency(dep_name):
                missing[dep_name] = {
                    "install": dep_info["install_command"],
                    "required_for": dep_info["required_for"]
                }
        return missing

    @classmethod
    def print_installation_summary(cls):
        """Print summary of available and missing dependencies."""
        print("\n" + "=" * 60)
        print("📦 Dependency Status Summary")
        print("=" * 60)

        available = []
        missing = []

        for dep_name, dep_info in cls.OPTIONAL_DEPENDENCIES.items():
            if cls.has_dependency(dep_name):
                available.append(dep_name)
            else:
                missing.append((dep_name, dep_info))

        print("\n✓ Available Dependencies:")
        for dep in available:
            print(f"  • {dep}")

        if missing:
            print("\n✗ Missing Optional Dependencies:")
            for dep_name, dep_info in missing:
                print(f"  • {dep_name}")
                print(f"    Install: {dep_info['install_command']}")
                print(f"    Needed for: {dep_info['required_for']}")
        else:
            print("\n✓ All optional dependencies are installed!")

        print("\n" + "=" * 60)


def require_framework(framework: str):
    """
    Decorator to require a specific ML framework.

    Args:
        framework: Framework name (pytorch, tensorflow, sklearn)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            framework_map = {
                "pytorch": "torch",
                "tensorflow": "tensorflow",
                "keras": "tensorflow",
                "sklearn": "sklearn",
                "scikit-learn": "sklearn"
            }

            dep_name = framework_map.get(framework, framework)

            if not DependencyOptimizer.has_dependency(dep_name):
                raise ImportError(
                    f"Framework '{framework}' is required but not installed.\n"
                    f"Install using: {DependencyOptimizer.OPTIONAL_DEPENDENCIES[dep_name]['install_command']}"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


def optional_import(dep_name: str, fallback=None):
    """
    Try to import a dependency, fall back to alternative if needed.

    Args:
        dep_name: Name of dependency to import
        fallback: Fallback value if import fails

    Returns:
        Imported module or fallback
    """
    try:
        return DependencyOptimizer.require_dependency(dep_name)
    except ImportError:
        if fallback is not None:
            return fallback
        raise


class DependencyAwareConfig:
    """Configuration that adapts based on available dependencies."""

    def __init__(self):
        """Initialize dependency-aware config."""
        self._cache = {}

    def get_available_models(self) -> Dict[str, list]:
        """Get available model architectures based on installed frameworks."""
        if "models" in self._cache:
            return self._cache["models"]

        available_frameworks = DependencyOptimizer.get_available_frameworks()

        models = {
            "image-classification": [],
            "text-classification": [],
            "regression": [],
            "clustering": [],
            "nlp": []
        }

        if "pytorch" in available_frameworks:
            models["image-classification"].extend(["resnet18", "resnet50", "vgg16"])
            models["text-classification"].extend(["lstm", "bert"])
            models["regression"].extend(["mlp", "linear"])
            models["nlp"].extend(["transformer", "gpt"])

        if "tensorflow" in available_frameworks:
            models["image-classification"].extend(["mobilenet", "inception"])
            models["text-classification"].extend(["bert_tf", "lstm_tf"])
            models["regression"].extend(["dense"])

        if "sklearn" in available_frameworks:
            models["classification"].extend(["random-forest", "svm", "logistic-regression"])
            models["regression"].extend(["linear", "random-forest"])
            models["clustering"].extend(["kmeans", "dbscan"])

        self._cache["models"] = models
        return models

    def get_recommended_framework(self, task: str) -> Optional[str]:
        """Get recommended framework for a task."""
        available = DependencyOptimizer.get_available_frameworks()

        recommendations = {
            "image-classification": ["pytorch", "tensorflow"],
            "text-classification": ["pytorch", "tensorflow"],
            "nlp": ["pytorch", "tensorflow"],
            "regression": ["pytorch", "tensorflow", "sklearn"],
            "clustering": ["sklearn"],
            "time-series": ["pytorch", "tensorflow"]
        }

        for framework in recommendations.get(task, []):
            if framework in available:
                return framework

        return available[0] if available else None

    def validate_setup(self) -> Dict[str, Any]:
        """Validate NoLess installation and dependencies."""
        return {
            "available_frameworks": DependencyOptimizer.get_available_frameworks(),
            "missing_dependencies": DependencyOptimizer.get_missing_dependencies(),
            "ready_to_use": len(DependencyOptimizer.get_available_frameworks()) > 0
        }
