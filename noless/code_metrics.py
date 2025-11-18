"""Code quality metrics analysis for generated code."""

import ast
import re
from typing import Dict, List, Optional, Any
from noless.schemas import CodeMetrics


class CodeMetricsAnalyzer:
    """Analyze code quality metrics."""

    def __init__(self):
        """Initialize metrics analyzer."""
        self.metrics: Dict[str, Any] = {}

    def analyze(self, code: str) -> CodeMetrics:
        """
        Analyze code and return metrics.

        Args:
            code: Python code to analyze

        Returns:
            CodeMetrics object with analysis results
        """
        self.metrics = {
            "lines_of_code": self._count_lines(code),
            "cyclomatic_complexity": self._calculate_complexity(code),
            "functions": self._count_functions(code),
            "classes": self._count_classes(code),
            "comments_ratio": self._calculate_comment_ratio(code),
            "duplicated_lines": self._find_duplicated_lines(code),
            "type_hints_coverage": self._calculate_type_hints_coverage(code),
        }

        return CodeMetrics(
            lines_of_code=self.metrics["lines_of_code"],
            cyclomatic_complexity=self.metrics["cyclomatic_complexity"],
            functions=self.metrics["functions"],
            classes=self.metrics["classes"],
            comments_ratio=self.metrics["comments_ratio"],
            duplicated_lines=self.metrics["duplicated_lines"],
            type_hints_coverage=self.metrics["type_hints_coverage"],
        )

    def _count_lines(self, code: str) -> int:
        """Count non-empty lines of code."""
        lines = code.split("\n")
        return sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

    def _calculate_complexity(self, code: str) -> float:
        """Calculate average cyclomatic complexity."""
        try:
            tree = ast.parse(code)
            complexities = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = 1
                    for child in ast.walk(node):
                        if isinstance(
                            child,
                            (
                                ast.If,
                                ast.For,
                                ast.While,
                                ast.ExceptHandler,
                                ast.BoolOp,
                            ),
                        ):
                            complexity += 1
                    complexities.append(complexity)

            return (
                sum(complexities) / len(complexities) if complexities else 1.0
            )
        except SyntaxError:
            return 0.0

    def _count_functions(self, code: str) -> int:
        """Count function definitions."""
        try:
            tree = ast.parse(code)
            return sum(
                1
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            )
        except SyntaxError:
            return 0

    def _count_classes(self, code: str) -> int:
        """Count class definitions."""
        try:
            tree = ast.parse(code)
            return sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
        except SyntaxError:
            return 0

    def _calculate_comment_ratio(self, code: str) -> float:
        """Calculate ratio of comment lines to code lines."""
        lines = code.split("\n")
        comment_lines = sum(
            1 for line in lines if line.strip().startswith("#")
        )
        code_lines = sum(1 for line in lines if line.strip())

        return (
            comment_lines / code_lines if code_lines > 0 else 0.0
        )

    def _find_duplicated_lines(self, code: str) -> int:
        """Find duplicated code segments (simple check)."""
        lines = code.split("\n")
        cleaned = [
            line.strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]

        duplicates = 0
        seen = set()
        for line in cleaned:
            if line in seen:
                duplicates += 1
            seen.add(line)

        return duplicates

    def _calculate_type_hints_coverage(self, code: str) -> float:
        """Calculate percentage of functions with type hints."""
        try:
            tree = ast.parse(code)
            functions = [
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]

            if not functions:
                return 1.0

            with_hints = sum(
                1
                for func in functions
                if func.returns is not None
                or any(arg.annotation for arg in func.args.args)
            )

            return with_hints / len(functions)
        except SyntaxError:
            return 0.0

    def get_quality_grade(self) -> str:
        """Get overall quality grade (A-F)."""
        score = self._calculate_quality_score()

        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _calculate_quality_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        score = 100

        # Penalize high complexity
        complexity = self.metrics.get("cyclomatic_complexity", 1.0)
        if complexity > 5:
            score -= min(20, (complexity - 5) * 2)

        # Reward good comment ratio
        comment_ratio = self.metrics.get("comments_ratio", 0.0)
        score += min(10, comment_ratio * 50)

        # Penalize duplicated code
        duplicates = self.metrics.get("duplicated_lines", 0)
        score -= min(15, duplicates)

        # Reward type hints
        type_coverage = self.metrics.get("type_hints_coverage", 0.0)
        score += min(10, type_coverage * 30)

        return max(0, min(100, score))

    def format_report(self) -> str:
        """Format metrics as readable report."""
        lines = [
            "📊 Code Quality Metrics",
            "=" * 40,
            f"Lines of Code: {self.metrics.get('lines_of_code', 0)}",
            f"Functions: {self.metrics.get('functions', 0)}",
            f"Classes: {self.metrics.get('classes', 0)}",
            f"Complexity: {self.metrics.get('cyclomatic_complexity', 0):.2f}",
            f"Comment Ratio: {self.metrics.get('comments_ratio', 0):.1%}",
            f"Duplicated Lines: {self.metrics.get('duplicated_lines', 0)}",
            f"Type Hints Coverage: {self.metrics.get('type_hints_coverage', 0):.1%}",
            f"\nQuality Grade: {self.get_quality_grade()}",
            f"Score: {self._calculate_quality_score():.1f}/100",
        ]
        return "\n".join(lines)
