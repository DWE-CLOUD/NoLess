"""Enhanced error detection including security and performance issues."""

import ast
import re
from typing import List, Dict, Optional, Any
from noless.schemas import SecurityIssue, PerformanceIssue


class SecurityAnalyzer:
    """Detect security vulnerabilities in code."""

    SECURITY_PATTERNS = {
        "hardcoded_secret": {
            "patterns": [
                r"api[_-]?key\s*=\s*['\"]",
                r"password\s*=\s*['\"]",
                r"secret\s*=\s*['\"]",
                r"token\s*=\s*['\"]",
                r"aws[_-]?access[_-]?key\s*=\s*['\"]",
            ],
            "severity": "critical",
            "message": "Hardcoded secret or credential found",
        },
        "eval_usage": {
            "patterns": [r"\beval\s*\(", r"\bexec\s*\("],
            "severity": "critical",
            "message": "Use of eval/exec is dangerous - consider safer alternatives",
        },
        "unvalidated_input": {
            "patterns": [r"os\.system\s*\(", r"subprocess\.call\s*\("],
            "severity": "high",
            "message": "Unvalidated shell command execution",
        },
        "pickle_usage": {
            "patterns": [r"pickle\.loads\s*\(", r"pickle\.load\s*\("],
            "severity": "high",
            "message": "pickle.loads with untrusted data is unsafe",
        },
        "sql_injection": {
            "patterns": [r"execute\s*\(\s*f['\"]", r'execute\s*\(\s*".*\{'],
            "severity": "critical",
            "message": "Potential SQL injection with f-string or format",
        },
    }

    def analyze(self, code: str) -> List[SecurityIssue]:
        """
        Analyze code for security issues.

        Args:
            code: Python code to analyze

        Returns:
            List of security issues found
        """
        issues = []

        # Check pattern-based issues
        for issue_type, config in self.SECURITY_PATTERNS.items():
            for pattern in config["patterns"]:
                for line_num, line in enumerate(code.split("\n"), 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(
                            SecurityIssue(
                                type=issue_type,
                                severity=config["severity"],
                                message=config["message"],
                                line=line_num,
                                fix=self._get_fix(issue_type),
                            )
                        )

        # AST-based analysis
        issues.extend(self._check_ast_issues(code))

        return issues

    def _check_ast_issues(self, code: str) -> List[SecurityIssue]:
        """Check AST for security issues."""
        issues = []
        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                # Check for assert statements (disabled in production)
                if isinstance(node, ast.Assert):
                    issues.append(
                        SecurityIssue(
                            type="assertion",
                            severity="medium",
                            message="Assertions can be disabled with -O flag, avoid for critical checks",
                            line=node.lineno,
                            fix="Use proper exception handling instead of assertions",
                        )
                    )

                # Check for requests without timeout
                if isinstance(node, ast.Call):
                    func_name = self._get_call_name(node)
                    if func_name in ("requests.get", "requests.post", "requests.request"):
                        if not self._has_timeout_arg(node):
                            issues.append(
                                SecurityIssue(
                                    type="missing_timeout",
                                    severity="medium",
                                    message="HTTP request without timeout could hang indefinitely",
                                    line=node.lineno,
                                    fix="Add timeout parameter: requests.get(url, timeout=30)",
                                )
                            )

        except SyntaxError:
            pass

        return issues

    def _get_call_name(self, node: ast.Call) -> Optional[str]:
        """Get function name from Call node."""
        if isinstance(node.func, ast.Attribute):
            return f"{node.func.attr}"
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return None

    def _has_timeout_arg(self, node: ast.Call) -> bool:
        """Check if function call has timeout argument."""
        return any(
            (isinstance(arg, ast.keyword) and arg.arg == "timeout")
            for arg in node.keywords
        )

    def _get_fix(self, issue_type: str) -> str:
        """Get suggested fix for issue type."""
        fixes = {
            "hardcoded_secret": "Use environment variables: os.getenv('API_KEY')",
            "eval_usage": "Use ast.literal_eval() or json.loads() for safe parsing",
            "unvalidated_input": "Use subprocess with shell=False and validate inputs",
            "pickle_usage": "Use json or other safe serialization formats",
            "sql_injection": "Use parameterized queries: execute(query, params)",
        }
        return fixes.get(issue_type, "Review and fix this security issue")


class PerformanceAnalyzer:
    """Detect performance anti-patterns in code."""

    def analyze(self, code: str) -> List[PerformanceIssue]:
        """
        Analyze code for performance issues.

        Args:
            code: Python code to analyze

        Returns:
            List of performance issues found
        """
        issues = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                # Check for list operations in loops
                if isinstance(node, ast.For):
                    issues.extend(self._check_loop_patterns(node))

                # Check for string concatenation in loops
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                    issues.extend(self._check_string_concat(node))

                # Check for deep nesting
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    depth = self._get_nesting_depth(node)
                    if depth > 4:
                        issues.append(
                            PerformanceIssue(
                                type="deep_nesting",
                                location=node.name,
                                message=f"High nesting depth ({depth}) reduces readability and performance",
                                impact="medium",
                                suggestion="Refactor into smaller functions",
                            )
                        )

                # Check for list comprehension vs append
                if isinstance(node, (ast.ListComp, ast.DictComp)):
                    issues.extend(self._check_comprehension(node))

        except SyntaxError:
            pass

        # Pattern-based checks
        issues.extend(self._check_patterns(code))

        return issues

    def _check_loop_patterns(self, node: ast.For) -> List[PerformanceIssue]:
        """Check for inefficient loop patterns."""
        issues = []

        # Check for list operations inside loop
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    if child.func.attr in ("append", "insert", "remove"):
                        issues.append(
                            PerformanceIssue(
                                type="inefficient_loop",
                                message="List modification inside loop is inefficient",
                                impact="high",
                                suggestion="Use list comprehension instead: [modify(x) for x in items]",
                            )
                        )

        return issues

    def _check_string_concat(self, node: ast.BinOp) -> List[PerformanceIssue]:
        """Check for inefficient string concatenation."""
        issues = []

        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            # String concatenation detected
            parent = getattr(node, "_parent", None)
            if isinstance(parent, ast.For):
                issues.append(
                    PerformanceIssue(
                        type="string_concat",
                        message="String concatenation in loop is slow",
                        impact="high",
                        suggestion="Use list + join() instead: ''.join([...])",
                    )
                )

        return issues

    def _check_comprehension(self, node: Any) -> List[PerformanceIssue]:
        """Verify comprehension usage is appropriate."""
        # Comprehensions are generally good, so this validates good practices
        return []

    def _check_patterns(self, code: str) -> List[PerformanceIssue]:
        """Check for performance patterns via regex."""
        issues = []

        # Check for inefficient imports
        if re.search(r"from\s+\*\s+import", code):
            issues.append(
                PerformanceIssue(
                    type="wildcard_import",
                    message="Wildcard imports reduce clarity and can cause namespace pollution",
                    impact="low",
                    suggestion="Import specific items: from module import func1, func2",
                )
            )

        # Check for debug prints
        if re.search(r"print\s*\(\s*['\"]debug", code, re.IGNORECASE):
            issues.append(
                PerformanceIssue(
                    type="debug_print",
                    message="Debug print statements left in code",
                    impact="low",
                    suggestion="Remove debug prints or use logging module",
                )
            )

        # Check for list() conversion of already-iterables
        if re.search(r"list\s*\(\s*\[\s*", code):
            issues.append(
                PerformanceIssue(
                    type="redundant_conversion",
                    message="Converting list literal to list is redundant",
                    impact="low",
                    suggestion="Remove list() conversion from list literals",
                )
            )

        return issues

    def _get_nesting_depth(self, node: ast.AST) -> int:
        """Get maximum nesting depth in a function."""
        max_depth = 0

        for child in ast.walk(node):
            depth = 0
            current = child
            while hasattr(current, "_parent"):
                depth += 1
                current = getattr(current, "_parent")
            max_depth = max(max_depth, depth)

        return max_depth


class ErrorDetector:
    """Combined error detection with security and performance analysis."""

    def __init__(self):
        """Initialize error detector."""
        self.security_analyzer = SecurityAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()

    def analyze(self, code: str) -> Dict[str, Any]:
        """
        Complete error analysis of code.

        Args:
            code: Python code to analyze

        Returns:
            Dictionary with security_issues and performance_issues
        """
        return {
            "security_issues": self.security_analyzer.analyze(code),
            "performance_issues": self.performance_analyzer.analyze(code),
        }

    def format_report(self, analysis: Dict[str, Any]) -> str:
        """Format analysis results as readable report."""
        lines = ["🔍 Error & Issue Detection Report", "=" * 40]

        security_issues = analysis.get("security_issues", [])
        if security_issues:
            lines.append(f"\n🔒 Security Issues ({len(security_issues)}):")
            for issue in security_issues:
                lines.append(f"  [{issue.severity.upper()}] {issue.message}")
                if issue.fix:
                    lines.append(f"    Fix: {issue.fix}")
        else:
            lines.append("\n🔒 Security: ✓ No issues found")

        performance_issues = analysis.get("performance_issues", [])
        if performance_issues:
            lines.append(f"\n⚡ Performance Issues ({len(performance_issues)}):")
            for issue in performance_issues:
                lines.append(f"  [{issue.impact.upper()}] {issue.message}")
                if issue.suggestion:
                    lines.append(f"    Suggestion: {issue.suggestion}")
        else:
            lines.append("\n⚡ Performance: ✓ No issues found")

        return "\n".join(lines)
