"""Output filtering and dry-run modes for NoLess."""

from typing import Dict, List, Optional, Any
from enum import Enum


class OutputMode(Enum):
    """Output mode for code generation."""

    FULL = "full"  # Generate everything
    ANALYSIS_ONLY = "analysis_only"  # Only return analysis, no code generation
    DRY_RUN = "dry_run"  # Preview what would be generated
    SUMMARY = "summary"  # Only return summary of changes


class OutputFilter:
    """Filters output based on specified criteria."""

    def __init__(self, mode: OutputMode = OutputMode.FULL):
        """
        Initialize output filter.

        Args:
            mode: Output mode to use
        """
        self.mode = mode

    def filter_validation_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter validation results based on mode.

        Args:
            result: Original validation result

        Returns:
            Filtered result
        """
        if self.mode == OutputMode.ANALYSIS_ONLY:
            # Return only analysis, remove generated code
            return {
                "valid": result.get("valid"),
                "issues": result.get("issues", []),
                "suggestions": result.get("suggestions", []),
                "metrics": result.get("metrics"),
                "static_issues": result.get("static_issues", [])
                # Note: improved_code is NOT included
            }

        elif self.mode == OutputMode.DRY_RUN:
            # Include code preview but mark as preview
            filtered = result.copy()
            if filtered.get("improved_code"):
                # Only include first 10 lines as preview
                lines = filtered["improved_code"].split('\n')[:10]
                filtered["improved_code_preview"] = '\n'.join(lines)
                if len(filtered["improved_code"].split('\n')) > 10:
                    filtered["improved_code_preview"] += "\n... (truncated - use FULL mode to see all)"
                del filtered["improved_code"]
            return filtered

        elif self.mode == OutputMode.SUMMARY:
            # Only return summary
            return {
                "valid": result.get("valid"),
                "issue_count": len(result.get("issues", [])),
                "suggestion_count": len(result.get("suggestions", [])),
                "has_improvements": bool(result.get("improved_code")),
                "quality_grade": self._extract_grade(result)
            }

        else:  # FULL mode
            return result

    def filter_generation_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter generation results based on mode.

        Args:
            result: Original generation result

        Returns:
            Filtered result
        """
        if self.mode == OutputMode.ANALYSIS_ONLY:
            # Return only validation analysis, no generated files
            return {
                "analysis": result.get("validation_results", {}),
                "warnings": result.get("warnings", []),
                "files_would_be_created": result.get("files_created", [])
            }

        elif self.mode == OutputMode.DRY_RUN:
            # Show preview of what would be generated
            preview = {
                "project_dir": result.get("project_dir"),
                "files_that_would_be_created": result.get("files_created", []),
                "file_previews": {}
            }

            # Add previews of each file
            for file_path, content in result.get("file_contents", {}).items():
                if isinstance(content, str):
                    lines = content.split('\n')[:15]
                    preview["file_previews"][file_path] = {
                        "preview": '\n'.join(lines),
                        "total_lines": len(content.split('\n')),
                        "truncated": len(content.split('\n')) > 15
                    }

            return preview

        elif self.mode == OutputMode.SUMMARY:
            return {
                "success": result.get("success"),
                "project_dir": result.get("project_dir"),
                "files_created": len(result.get("files_created", [])),
                "validation_status": "passed" if all(
                    v.get("valid") for v in result.get("validation_results", {}).values()
                ) else "needs_attention"
            }

        else:  # FULL mode
            return result

    @staticmethod
    def _extract_grade(result: Dict[str, Any]) -> Optional[str]:
        """Extract quality grade from metrics."""
        metrics = result.get("metrics", {})
        # This would ideally come from code_metrics module
        return metrics.get("grade", "unknown")


class DryRunGenerator:
    """Generate dry-run previews without actual file creation."""

    @staticmethod
    def preview_project_generation(
        task: str,
        framework: str,
        dataset: str,
        output_dir: str
    ) -> Dict[str, Any]:
        """
        Generate preview of what would be created.

        Args:
            task: ML task type
            framework: ML framework
            dataset: Dataset name
            output_dir: Output directory

        Returns:
            Dry-run preview
        """
        return {
            "dry_run": True,
            "project_dir": output_dir,
            "files_that_would_be_created": [
                "config.yaml",
                "model.py",
                "train.py",
                "test_model.py",
                "requirements.txt",
                "README.md"
            ],
            "configuration": {
                "task": task,
                "framework": framework,
                "dataset": dataset
            },
            "estimated_generation_time": "~30 seconds",
            "notes": [
                "Use mode=FULL to actually generate files",
                "Files will be validated before creation"
            ]
        }

    @staticmethod
    def preview_model_code(
        task: str,
        framework: str,
        architecture: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Preview what model.py would contain.

        Args:
            task: ML task type
            framework: ML framework
            architecture: Model architecture

        Returns:
            Code preview
        """
        previews = {
            ("image-classification", "pytorch"): """
class ImageClassifier(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(...)
        self.classifier = nn.Sequential(...)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ...
""",
            ("text-classification", "pytorch"): """
class TextClassifier(nn.Module):
    def __init__(self, vocab_size: int, num_classes: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, 128)
        self.lstm = nn.LSTM(128, 256, batch_first=True)
        self.classifier = nn.Linear(256, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ...
""",
            ("regression", "pytorch"): """
class RegressionModel(nn.Module):
    def __init__(self, input_size: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        ...
"""
        }

        key = (task, framework)
        code_preview = previews.get(key, "# Custom model template will be generated")

        return {
            "dry_run": True,
            "model_preview": code_preview,
            "total_lines_estimated": 50,
            "configuration": {
                "task": task,
                "framework": framework,
                "architecture": architecture
            }
        }


class OutputSelector:
    """Select which components to include in output."""

    def __init__(self):
        """Initialize output selector."""
        self.include_code = True
        self.include_metrics = True
        self.include_issues = True
        self.include_suggestions = True
        self.include_security_analysis = True
        self.include_performance_analysis = True
        self.include_improved_code = True
        self.max_issues_shown = 10
        self.max_suggestions_shown = 5

    def configure(self, **kwargs):
        """Configure output selection."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def filter_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter result based on configuration.

        Args:
            result: Original result

        Returns:
            Filtered result
        """
        filtered = {}

        if self.include_code:
            filtered["improved_code"] = result.get("improved_code")

        if self.include_metrics:
            filtered["metrics"] = result.get("metrics")

        if self.include_issues:
            issues = result.get("issues", [])
            filtered["issues"] = issues[:self.max_issues_shown]
            if len(issues) > self.max_issues_shown:
                filtered["issues_truncated"] = f"{len(issues) - self.max_issues_shown} more issues"

        if self.include_suggestions:
            suggestions = result.get("suggestions", [])
            filtered["suggestions"] = suggestions[:self.max_suggestions_shown]
            if len(suggestions) > self.max_suggestions_shown:
                filtered["suggestions_truncated"] = f"{len(suggestions) - self.max_suggestions_shown} more suggestions"

        if self.include_security_analysis:
            filtered["security_issues"] = result.get("security_issues")

        if self.include_performance_analysis:
            filtered["performance_issues"] = result.get("performance_issues")

        filtered["valid"] = result.get("valid")

        return filtered
