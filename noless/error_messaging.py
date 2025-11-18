"""Improved error messages with actionable suggestions."""

from typing import Dict, List, Optional, Any
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ErrorMessageFormatter:
    """Formats errors with actionable suggestions and documentation links."""

    ERROR_SUGGESTIONS = {
        "ModuleNotFoundError": {
            "message": "Missing required module",
            "suggestion": "Install the missing module using: pip install {module_name}",
            "docs": "https://docs.python.org/3/library/importlib.html"
        },
        "SyntaxError": {
            "message": "Code has syntax errors",
            "suggestion": "Check for missing colons, parentheses, or indentation issues. Line: {line}",
            "docs": "https://docs.python.org/3/tutorial/errors.html"
        },
        "TypeError": {
            "message": "Type mismatch or incompatible types",
            "suggestion": "Ensure function arguments match expected types. Consider adding type hints.",
            "docs": "https://docs.python.org/3/library/typing.html"
        },
        "ValueError": {
            "message": "Invalid value provided",
            "suggestion": "Validate input values before using them. Add error handling with try-except.",
            "docs": "https://docs.python.org/3/tutorial/errors.html"
        },
        "ImportError": {
            "message": "Failed to import module",
            "suggestion": "Check module name spelling or install missing package. pip install {module}",
            "docs": "https://docs.python.org/3/library/importlib.html"
        },
        "KeyError": {
            "message": "Key not found in dictionary",
            "suggestion": "Use .get() method with default value or check if key exists before accessing",
            "docs": "https://docs.python.org/3/tutorial/datastructures.html#dictionaries"
        },
        "IndexError": {
            "message": "Index out of range",
            "suggestion": "Check list/array length before accessing. Use len() to validate index.",
            "docs": "https://docs.python.org/3/tutorial/introduction.html#lists"
        },
        "AttributeError": {
            "message": "Object has no attribute",
            "suggestion": "Check if attribute exists. Use hasattr() or handle AttributeError.",
            "docs": "https://docs.python.org/3/tutorial/classes.html"
        },
        "ConnectionError": {
            "message": "Failed to connect to server/database",
            "suggestion": "Check connection parameters, network connectivity, and add retry logic.",
            "docs": "https://docs.python.org/3/library/socket.html"
        },
        "TimeoutError": {
            "message": "Operation timed out",
            "suggestion": "Increase timeout duration or optimize the operation. Add timeout handling.",
            "docs": "https://docs.python.org/3/library/asyncio.html"
        }
    }

    @classmethod
    def format_error(
        cls,
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Format an error with suggestions.

        Args:
            error_type: Type of error (e.g., 'SyntaxError')
            error_message: Error message text
            context: Additional context information

        Returns:
            Formatted error with suggestions
        """
        context = context or {}

        suggestion_info = cls.ERROR_SUGGESTIONS.get(error_type, {})

        formatted = {
            "error_type": error_type,
            "message": error_message,
            "severity": cls._determine_severity(error_type),
            "description": suggestion_info.get("message", "An error occurred"),
            "suggestion": suggestion_info.get("suggestion", "Review the error message and traceback"),
            "documentation": suggestion_info.get("docs", ""),
            "context": context
        }

        return formatted

    @classmethod
    def _determine_severity(cls, error_type: str) -> str:
        """Determine error severity based on type."""
        critical_errors = {
            "SyntaxError", "IndentationError", "SystemError",
            "MemoryError", "RecursionError"
        }
        error_errors = {
            "TypeError", "ValueError", "KeyError", "IndexError",
            "ImportError", "ModuleNotFoundError"
        }

        if error_type in critical_errors:
            return ErrorSeverity.CRITICAL.value
        elif error_type in error_errors:
            return ErrorSeverity.ERROR.value
        else:
            return ErrorSeverity.WARNING.value

    @classmethod
    def format_for_display(cls, formatted_error: Dict[str, Any]) -> str:
        """
        Format error for display to user.

        Args:
            formatted_error: Formatted error dictionary

        Returns:
            Human-readable error message
        """
        lines = [
            f"[bold red]ERROR[/bold red]: {formatted_error['error_type']}",
            f"Message: {formatted_error['message']}",
            f"\n[yellow]Why this happened:[/yellow]",
            f"  {formatted_error['description']}",
            f"\n[green]How to fix it:[/green]",
            f"  {formatted_error['suggestion']}"
        ]

        if formatted_error.get("documentation"):
            lines.append(f"\n[cyan]Learn more:[/cyan]")
            lines.append(f"  {formatted_error['documentation']}")

        return "\n".join(lines)


class ValidationError:
    """Enhanced validation error with actionable feedback."""

    def __init__(
        self,
        error_type: str,
        severity: ErrorSeverity,
        message: str,
        suggestion: str,
        line_number: Optional[int] = None
    ):
        """
        Initialize validation error.

        Args:
            error_type: Type of validation error
            severity: Severity level
            message: Error message
            suggestion: How to fix it
            line_number: Line number where error occurred
        """
        self.error_type = error_type
        self.severity = severity
        self.message = message
        self.suggestion = suggestion
        self.line_number = line_number

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.error_type,
            "severity": self.severity.value,
            "message": self.message,
            "suggestion": self.suggestion,
            "line": self.line_number
        }

    def __str__(self) -> str:
        location = f" (line {self.line_number})" if self.line_number else ""
        return f"[{self.severity.value}] {self.error_type}{location}: {self.message}\nFix: {self.suggestion}"


class ProgressTracker:
    """Track and report progress during code generation and validation."""

    def __init__(self, total_steps: int):
        """
        Initialize progress tracker.

        Args:
            total_steps: Total number of steps
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.step_details: List[Dict[str, Any]] = []

    def start_step(self, step_name: str, description: str = ""):
        """
        Mark start of a step.

        Args:
            step_name: Name of the step
            description: Step description
        """
        self.current_step += 1
        step_info = {
            "step": self.current_step,
            "name": step_name,
            "description": description,
            "status": "IN_PROGRESS"
        }
        self.step_details.append(step_info)

    def complete_step(self, result: Optional[Any] = None):
        """
        Mark step as complete.

        Args:
            result: Optional result from step
        """
        if self.step_details:
            self.step_details[-1]["status"] = "COMPLETED"
            if result:
                self.step_details[-1]["result"] = result

    def fail_step(self, error: str):
        """
        Mark step as failed.

        Args:
            error: Error message
        """
        if self.step_details:
            self.step_details[-1]["status"] = "FAILED"
            self.step_details[-1]["error"] = error

    def get_progress_percentage(self) -> float:
        """Get current progress as percentage."""
        return (self.current_step / self.total_steps) * 100

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get progress summary."""
        return {
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "percentage": self.get_progress_percentage(),
            "steps": self.step_details
        }

    def format_progress_report(self) -> str:
        """Format progress as readable report."""
        lines = [f"\n📊 Progress Report: {self.current_step}/{self.total_steps} steps"]
        lines.append("=" * 50)

        for step in self.step_details:
            status_icon = {
                "COMPLETED": "✓",
                "IN_PROGRESS": "→",
                "FAILED": "✗"
            }.get(step["status"], "?")

            lines.append(f"{status_icon} Step {step['step']}: {step['name']}")
            if step.get("description"):
                lines.append(f"    {step['description']}")
            if step.get("error"):
                lines.append(f"    Error: {step['error']}")

        lines.append("=" * 50)
        return "\n".join(lines)
