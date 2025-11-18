#!/usr/bin/env python3
"""Test script for all NoLess optimization features."""

import sys
import time
from pathlib import Path
import os

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add noless to path
sys.path.insert(0, str(Path(__file__).parent))


def test_cache_manager():
    """Test caching system."""
    print("\n🧪 Testing Cache Manager...")
    try:
        from noless.cache_manager import get_cache_manager

        cache = get_cache_manager()

        # Test set/get
        cache.set("test_key", {"data": "test_value"}, category="test")
        result = cache.get("test_key")
        assert result == {"data": "test_value"}, "Cache get/set failed"
        print("   ✓ Set/Get works")

        # Test cache stats
        stats = cache.get_stats()
        assert stats["valid_entries"] > 0, "Cache stats failed"
        print("   ✓ Cache stats works")

        # Test get_or_compute
        def expensive_op():
            return {"computed": True}

        result = cache.get_or_compute("compute_key", expensive_op, "test")
        assert result["computed"], "get_or_compute failed"
        print("   ✓ get_or_compute works")

        # Test cleanup
        cleaned = cache.cleanup_expired()
        print(f"   ✓ Cleanup works (removed {cleaned} expired items)")

        # Test invalidation
        cache.invalidate(category="test")
        print("   ✓ Invalidation works")

        print("✅ Cache Manager: PASSED\n")
        return True
    except Exception as e:
        print(f"❌ Cache Manager: FAILED - {e}\n")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("🧪 Testing Pydantic Schemas...")
    try:
        from noless.schemas import (
            CodeIssue,
            CodeSuggestion,
            CodeReviewResult,
            CodeMetrics,
            SecurityIssue,
            PerformanceIssue,
        )

        # Test CodeIssue
        issue = CodeIssue(
            severity="warning",
            message="Test issue",
            category="syntax",
            line=10,
        )
        assert issue.severity == "warning", "CodeIssue creation failed"
        print("   ✓ CodeIssue works")

        # Test CodeSuggestion
        suggestion = CodeSuggestion(
            title="Add type hints", description="Functions lack type hints", type="best-practice"
        )
        assert suggestion.title == "Add type hints", "CodeSuggestion creation failed"
        print("   ✓ CodeSuggestion works")

        # Test CodeReviewResult
        review = CodeReviewResult(valid=True, issues=[], suggestions=[])
        assert review.valid, "CodeReviewResult creation failed"
        print("   ✓ CodeReviewResult works")

        # Test CodeMetrics
        metrics = CodeMetrics(
            lines_of_code=100,
            cyclomatic_complexity=2.5,
            functions=5,
            classes=2,
            comments_ratio=0.15,
        )
        assert metrics.lines_of_code == 100, "CodeMetrics creation failed"
        print("   ✓ CodeMetrics works")

        # Test SecurityIssue
        sec_issue = SecurityIssue(
            type="hardcoded_secret", severity="critical", message="Found API key", line=5
        )
        assert sec_issue.severity == "critical", "SecurityIssue creation failed"
        print("   ✓ SecurityIssue works")

        # Test PerformanceIssue
        perf_issue = PerformanceIssue(
            type="inefficient_loop", message="Loop inefficiency detected", impact="medium"
        )
        assert perf_issue.impact == "medium", "PerformanceIssue creation failed"
        print("   ✓ PerformanceIssue works")

        print("✅ Pydantic Schemas: PASSED\n")
        return True
    except Exception as e:
        print(f"❌ Pydantic Schemas: FAILED - {e}\n")
        return False


def test_code_metrics():
    """Test code metrics analyzer."""
    print("🧪 Testing Code Metrics Analyzer...")
    try:
        from noless.code_metrics import CodeMetricsAnalyzer

        analyzer = CodeMetricsAnalyzer()

        test_code = '''
def hello(name: str) -> str:
    """Say hello."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    # Add two numbers
    return a + b

class Calculator:
    def multiply(self, x: int, y: int) -> int:
        return x * y
'''

        metrics = analyzer.analyze(test_code)
        assert metrics.lines_of_code > 0, "LOC counting failed"
        assert metrics.functions > 0, "Function counting failed"
        assert metrics.classes > 0, "Class counting failed"
        print(f"   ✓ Detected {metrics.functions} functions")
        print(f"   ✓ Detected {metrics.classes} classes")
        print(f"   ✓ Type hints coverage: {metrics.type_hints_coverage:.1%}")

        grade = analyzer.get_quality_grade()
        assert grade in "ABCDF", "Quality grading failed"
        print(f"   ✓ Quality grade: {grade}")

        print("✅ Code Metrics Analyzer: PASSED\n")
        return True
    except Exception as e:
        print(f"❌ Code Metrics Analyzer: FAILED - {e}\n")
        return False


def test_error_detection():
    """Test error and security detection."""
    print("🧪 Testing Error Detection...")
    try:
        from noless.error_detection import ErrorDetector, SecurityAnalyzer, PerformanceAnalyzer

        # Test SecurityAnalyzer
        security = SecurityAnalyzer()
        dangerous_code = '''
password = "secret123"
api_key = "key-12345"
eval(user_input)
'''
        sec_issues = security.analyze(dangerous_code)
        assert len(sec_issues) > 0, "Security analyzer found no issues"
        print(f"   ✓ Security analyzer found {len(sec_issues)} issues")

        # Test PerformanceAnalyzer
        performance = PerformanceAnalyzer()
        slow_code = '''
result = ""
for item in items:
    result = result + str(item)
'''
        perf_issues = performance.analyze(slow_code)
        print(f"   ✓ Performance analyzer ran successfully")

        # Test combined ErrorDetector
        detector = ErrorDetector()
        analysis = detector.analyze(dangerous_code)
        assert "security_issues" in analysis, "ErrorDetector missing security_issues"
        assert "performance_issues" in analysis, "ErrorDetector missing performance_issues"
        print("   ✓ Combined error detection works")

        print("✅ Error Detection: PASSED\n")
        return True
    except Exception as e:
        print(f"❌ Error Detection: FAILED - {e}\n")
        return False


def test_async_processor():
    """Test async processor (basic test)."""
    print("🧪 Testing Async Processor...")
    try:
        from noless.async_processor import AsyncProcessor

        processor = AsyncProcessor(max_workers=2)
        assert processor.max_workers == 2, "AsyncProcessor initialization failed"
        print("   ✓ AsyncProcessor initialized")

        processor.shutdown()
        print("   ✓ AsyncProcessor shutdown works")

        print("✅ Async Processor: PASSED\n")
        return True
    except Exception as e:
        print(f"❌ Async Processor: FAILED - {e}\n")
        return False


def test_optimization_toolkit():
    """Test optimization toolkit."""
    print("🧪 Testing Optimization Toolkit...")
    try:
        from noless.optimization_utils import get_toolkit

        toolkit = get_toolkit()
        assert toolkit is not None, "Toolkit creation failed"
        print("   ✓ Toolkit created")

        test_code = "def hello(): pass"
        analysis = toolkit.analyze_code(test_code)
        assert "metrics" in analysis or "security_issues" in analysis, "Toolkit analysis failed"
        print("   ✓ Code analysis works")

        stats = toolkit.get_cache_stats()
        print(f"   ✓ Cache stats: {stats.get('valid_entries', 0)} entries")

        toolkit.shutdown()
        print("   ✓ Toolkit shutdown works")

        print("✅ Optimization Toolkit: PASSED\n")
        return True
    except Exception as e:
        print(f"❌ Optimization Toolkit: FAILED - {e}\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🚀 NoLess Optimization Features Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Cache Manager", test_cache_manager()))
    results.append(("Pydantic Schemas", test_schemas()))
    results.append(("Code Metrics", test_code_metrics()))
    results.append(("Error Detection", test_error_detection()))
    results.append(("Async Processor", test_async_processor()))
    results.append(("Optimization Toolkit", test_optimization_toolkit()))

    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} - {name}")

    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All optimizations working correctly!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
