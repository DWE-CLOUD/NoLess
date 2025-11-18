"""Utility functions for accessing and managing optimizations."""

from typing import Optional, Dict, Any
from noless.cache_manager import get_cache_manager, CacheManager
from noless.async_processor import AsyncProcessor, RateLimiter, ParallelLLMProcessor
from noless.code_metrics import CodeMetricsAnalyzer
from noless.error_detection import ErrorDetector, SecurityAnalyzer, PerformanceAnalyzer


class OptimizationToolkit:
    """Centralized access to all optimization features."""

    def __init__(self, enable_all: bool = True):
        """
        Initialize optimization toolkit with all features.

        Args:
            enable_all: Whether to enable all features by default
        """
        self.enabled = enable_all
        self.cache = get_cache_manager() if enable_all else None
        self.async_processor = AsyncProcessor(max_workers=4) if enable_all else None
        self.metrics_analyzer = CodeMetricsAnalyzer() if enable_all else None
        self.error_detector = ErrorDetector() if enable_all else None
        self.security_analyzer = SecurityAnalyzer() if enable_all else None
        self.performance_analyzer = PerformanceAnalyzer() if enable_all else None

    def analyze_code(self, code: str, file_type: str = "python") -> Dict[str, Any]:
        """
        Perform complete code analysis including metrics and error detection.

        Args:
            code: Code to analyze
            file_type: Type of code (python, javascript, etc)

        Returns:
            Dictionary with all analysis results
        """
        results = {}

        if self.metrics_analyzer:
            results["metrics"] = self.metrics_analyzer.analyze(code).model_dump()

        if self.error_detector:
            analysis = self.error_detector.analyze(code)
            results["security_issues"] = [issue.dict() for issue in analysis.get("security_issues", [])]
            results["performance_issues"] = [issue.dict() for issue in analysis.get("performance_issues", [])]

        return results

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if self.cache:
            return self.cache.get_stats()
        return {}

    def clear_cache(self, category: Optional[str] = None) -> int:
        """
        Clear cache entries.

        Args:
            category: Specific category to clear (None = all)

        Returns:
            Number of entries cleared
        """
        if not self.cache:
            return 0

        if category:
            return self.cache.invalidate(category=category)
        else:
            self.cache.clear()
            return 0

    def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries."""
        if self.cache:
            return self.cache.cleanup_expired()
        return 0

    def get_report(self, code: str) -> str:
        """Get a formatted report of all analysis."""
        lines = ["=" * 60, "📋 Complete Code Analysis Report", "=" * 60]

        analysis = self.analyze_code(code)

        # Metrics section
        if "metrics" in analysis:
            metrics = analysis["metrics"]
            lines.append("\n📈 CODE METRICS")
            lines.append("-" * 40)
            lines.append(f"  Lines of Code: {metrics.get('lines_of_code', 0)}")
            lines.append(f"  Functions: {metrics.get('functions', 0)}")
            lines.append(f"  Classes: {metrics.get('classes', 0)}")
            lines.append(f"  Complexity: {metrics.get('cyclomatic_complexity', 0):.2f}")
            lines.append(f"  Type Hints: {metrics.get('type_hints_coverage', 0):.1%}")

        # Security issues
        if "security_issues" in analysis:
            security = analysis["security_issues"]
            lines.append("\n🔒 SECURITY ANALYSIS")
            lines.append("-" * 40)
            if security:
                for issue in security:
                    lines.append(f"  [{issue.get('severity', 'unknown').upper()}] {issue.get('type')}")
                    lines.append(f"    {issue.get('message')}")
            else:
                lines.append("  ✓ No security issues found")

        # Performance issues
        if "performance_issues" in analysis:
            performance = analysis["performance_issues"]
            lines.append("\n⚡ PERFORMANCE ANALYSIS")
            lines.append("-" * 40)
            if performance:
                for issue in performance:
                    lines.append(f"  [{issue.get('impact', 'unknown').upper()}] {issue.get('type')}")
                    lines.append(f"    {issue.get('message')}")
            else:
                lines.append("  ✓ No performance issues found")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)

    def shutdown(self) -> None:
        """Shutdown async processors."""
        if self.async_processor:
            self.async_processor.shutdown()


# Global toolkit instance
_toolkit: Optional[OptimizationToolkit] = None


def get_toolkit() -> OptimizationToolkit:
    """Get or create global optimization toolkit."""
    global _toolkit
    if _toolkit is None:
        _toolkit = OptimizationToolkit()
    return _toolkit


def enable_optimizations(enable_caching: bool = True, enable_metrics: bool = True, enable_error_detection: bool = True) -> None:
    """
    Enable/disable optimization features globally.

    Args:
        enable_caching: Enable caching layer
        enable_metrics: Enable code metrics analysis
        enable_error_detection: Enable error/security detection
    """
    global _toolkit
    _toolkit = OptimizationToolkit(enable_all=True)


def clear_all_caches() -> None:
    """Clear all caches."""
    toolkit = get_toolkit()
    toolkit.clear_cache()


def print_optimization_summary() -> None:
    """Print summary of optimization features enabled."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="🚀 NoLess Optimization Features", show_header=True)
    table.add_column("Feature", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Description", style="dim")

    toolkit = get_toolkit()

    features = [
        ("Caching System", "✓ Enabled" if toolkit.cache else "✗ Disabled", "SQLite-based cache for results"),
        (
            "Async Processing",
            "✓ Enabled" if toolkit.async_processor else "✗ Disabled",
            "Parallel LLM processing",
        ),
        ("Code Metrics", "✓ Enabled" if toolkit.metrics_analyzer else "✗ Disabled", "Complexity, type hints, etc"),
        (
            "Security Analysis",
            "✓ Enabled" if toolkit.security_analyzer else "✗ Disabled",
            "Vulnerability detection",
        ),
        (
            "Performance Analysis",
            "✓ Enabled" if toolkit.performance_analyzer else "✗ Disabled",
            "Performance anti-patterns",
        ),
    ]

    for feature, status, description in features:
        table.add_row(feature, status, description)

    console.print(table)
