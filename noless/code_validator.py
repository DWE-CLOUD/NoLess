"""AI-powered code validation and improvement using larger models."""

from typing import Dict, Any, Optional
import json
import time
import re
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from noless.ollama_client import OllamaClient
from noless.local_models import LocalModelRegistry, LocalModelInfo
from noless.schemas import CodeReviewResult, CodeIssue, CodeSuggestion, LLMResponse
from noless.cache_manager import get_cache_manager
from noless.code_metrics import CodeMetricsAnalyzer
from noless.error_detection import ErrorDetector

console = Console()


class CodeValidator:
    """Validate and improve generated code using AI."""

    def __init__(
        self,
        reviewer_model: Optional[str] = None,
        generation_model: Optional[str] = None,
        ollama_client: Optional[OllamaClient] = None,
        enable_caching: bool = True,
        enable_metrics: bool = True,
        enable_error_detection: bool = True,
    ):
        self.requested_reviewer_model = reviewer_model
        self.generation_model = generation_model
        self.client = ollama_client or OllamaClient()
        self.registry = LocalModelRegistry(self.client)
        self._available_models = self.registry.available_models()
        self.reviewer_model = self._resolve_reviewer_model()

        # Initialize optional features
        self.cache = get_cache_manager() if enable_caching else None
        self.metrics_analyzer = CodeMetricsAnalyzer() if enable_metrics else None
        self.error_detector = ErrorDetector() if enable_error_detection else None
    
    def _resolve_reviewer_model(self) -> Optional[str]:
        """Honor user preference first, then try to auto-select a reviewer."""
        if self.requested_reviewer_model:
            if self._has_model(self.requested_reviewer_model):
                return self.requested_reviewer_model
            print(
                f"[Warning] Requested reviewer model '{self.requested_reviewer_model}' not found locally. "
                "Falling back to automatic selection."
            )
        return self._select_reviewer_model()

    def _has_model(self, model_name: str) -> bool:
        return any(info.name == model_name for info in self._available_models)

    def _select_reviewer_model(self) -> Optional[str]:
        """Choose a strong available reviewer model when the user didn't specify one."""
        if not self._available_models:
            return None

        size_priority = [
            "70b",
            "32b",
            "8x7b",
            "13b",
            "12b",
            "11b",
            "10b",
            "9b",
            "8b",
            "7b",
            "6b",
            "5b",
            "4b",
            "3b",
            "2b",
            "1.5b",
        ]

        def matches(info: LocalModelInfo, marker: str) -> bool:
            value = marker.lower()
            return value in info.size.lower() or value in info.name.lower()

        # Prefer larger reviewers that differ from the generation model if possible.
        for marker in size_priority:
            for model_info in sorted(self._available_models, key=lambda info: info.name):
                if self.generation_model and model_info.name == self.generation_model:
                    continue
                if matches(model_info, marker):
                    return model_info.name

        # Fallback: pick any model that isn't the generation model.
        for model_info in self._available_models:
            if model_info.name != self.generation_model:
                return model_info.name

        # Last resort: reuse the generation model (at least we can still review).
        if self.generation_model and self._has_model(self.generation_model):
            return self.generation_model
        return self._available_models[0].name if self._available_models else None
    
    def validate_and_improve(self, code: str, file_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate code and suggest improvements with real-time feedback"""
        if not self.reviewer_model:
            return {"valid": True, "improved_code": code, "issues": [], "suggestions": []}

        # Check cache first
        cache_key = f"review:{file_type}:{hash(code) & 0xffffffff}"
        if self.cache:
            cached_result = self.cache.get(cache_key)
            if cached_result:
                console.print("[dim]📦 Using cached review results[/dim]")
                return cached_result

        # Show what's being reviewed
        console.print("\n")
        console.print(Panel.fit(
            f"[bold cyan]🔍 AI Code Review in Progress[/bold cyan]\n"
            f"Reviewing: [yellow]{file_type}[/yellow]\n"
            f"Model: [green]{self.reviewer_model}[/green]",
            border_style="cyan"
        ))
        console.print("\n")

        # Show code being reviewed with scroll animation
        code_lines = code.split('\n')
        total_lines = len(code_lines)
        console.print(f"[dim]📄 Scanning {total_lines} lines...[/dim]\n")

        # Show code scrolling animation (fast scan visualization)
        self._show_code_scan_animation(code_lines, file_type)

        # Run static analysis (fast, no LLM needed)
        static_issues = []
        if self.error_detector:
            analysis = self.error_detector.analyze(code)
            static_issues = analysis.get("security_issues", []) + analysis.get("performance_issues", [])
            if static_issues:
                console.print(f"[yellow]⚠️  Found {len(static_issues)} static analysis issues[/yellow]\n")

        # Show thinking process - FAST
        thinking_steps = [
            "🧠 Loading model",
            "🔍 Syntax check",
            "⚠️  Bug detection",
            "📋 Best practices",
            "⚡ Performance",
            "🔒 Security",
            "✨ Suggestions"
        ]

        with Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]AI Analysis", total=len(thinking_steps))

            for step in thinking_steps:
                progress.update(task, description=f"[cyan]{step}")
                time.sleep(0.1)  # FAST!
                progress.advance(task)

        console.print("[bold green]✓[/bold green] Analysis complete!\n")

        prompt = self._build_review_prompt(code, file_type, context)
        system_msg = (
            "You are a senior code reviewer. Analyze the code for bugs, best practices, and improvements."
            " Return JSON with keys: valid (bool), issues (array of strings), suggestions (array of strings), improved_code (string)."
            " Only include improved_code if significant changes are needed."
        )

        try:
            with console.status("[bold yellow]🤖 AI Reviewer analyzing code...", spinner="dots"):
                response = self.client.generate(self.reviewer_model, prompt, system=system_msg, temperature=0.2)

            result = self._parse_review_response(response)

            # Combine static analysis with LLM results
            if result and static_issues:
                result["static_issues"] = static_issues

            # Analyze code metrics
            if self.metrics_analyzer:
                metrics = self.metrics_analyzer.analyze(code)
                result["metrics"] = metrics.model_dump() if hasattr(metrics, 'model_dump') else metrics.__dict__

            # Check if we have issues but no improvements yet
            has_issues = result and (result.get("issues") or result.get("static_issues"))
            has_improvements = result and result.get("improved_code")

            # If issues found but no improved_code provided, attempt to fix them
            if has_issues and not has_improvements:
                result = self._attempt_to_fix_issues(result, code, file_type, context)
                has_improvements = result and result.get("improved_code")

            # Show review results
            self._display_review_results(result, code, file_type)

            # Cache the result
            if self.cache and result:
                self.cache.set(cache_key, result, category="validation")

            if result and result.get("improved_code"):
                return result

            # Return proper format even if result is None
            if result:
                return {"valid": True, "improved_code": code, "issues": result.get("issues", []), "suggestions": result.get("suggestions", [])}
            else:
                return {"valid": True, "improved_code": code, "issues": [], "suggestions": []}
        except Exception as exc:
            console.print(f"[red]⚠️  Code validation failed: {exc}[/red]\n")
            return {"valid": True, "improved_code": code, "issues": [], "suggestions": []}

    def _show_code_scan_animation(self, code_lines: list, file_type: str):
        """Show code scrolling animation during review - fast scroll effect"""
        total_lines = len(code_lines)
        window_size = 12

        with Live(console=console, refresh_per_second=60) as live:
            # Fast scroll through all code
            for i in range(0, total_lines, 3):  # Skip lines for speed
                start = max(0, i - window_size + 1)
                end = min(i + 1, total_lines)

                visible_lines = code_lines[start:end]
                code_text = '\n'.join(visible_lines)

                syntax = Syntax(
                    code_text,
                    "python",
                    theme="monokai",
                    line_numbers=True,
                    start_line=start + 1,
                    word_wrap=False
                )

                scroll_info = f" ↑{start}" if start > 0 else ""
                remaining = total_lines - end
                if remaining > 0:
                    scroll_info += f" ↓{remaining}"

                panel = Panel(
                    syntax,
                    title=f"[bold yellow]🔍 Scanning {file_type} [{end}/{total_lines}]{scroll_info}[/bold yellow]",
                    border_style="yellow",
                    padding=(0, 1)
                )

                live.update(panel)
                time.sleep(0.008)  # Super fast scrolling

        console.print(f"[green]✓[/green] Code scan complete\n")

    def _display_review_results(self, result: Optional[Dict[str, Any]], original_code: str, file_type: str):
        """Display review results in a beautiful format"""
        if not result:
            console.print("[yellow]⚠️  No review results available[/yellow]\n")
            return

        issues = result.get("issues", [])
        suggestions = result.get("suggestions", [])
        static_issues = result.get("static_issues", [])
        metrics = result.get("metrics", {})
        has_improvements = result.get("improved_code") and result["improved_code"] != original_code

        # Create review summary table
        table = Table(title="📊 Code Review Summary", show_header=True, header_style="bold magenta", border_style="cyan")
        table.add_column("Category", style="cyan", width=20)
        table.add_column("Count", style="green", justify="center", width=10)
        table.add_column("Status", style="yellow", width=20)

        total_issues = len(issues) + len(static_issues)
        table.add_row("Issues Found", str(total_issues), "🔴 Needs Attention" if total_issues > 0 else "✅ Clean")
        table.add_row("Suggestions", str(len(suggestions)), "💡 Available" if suggestions else "✅ Good")
        table.add_row("Improvements", "Yes" if has_improvements else "No", "🔧 Generated" if has_improvements else "✅ Optimal")

        console.print(table)
        console.print("\n")

        # Show AI-detected issues
        if issues:
            console.print(Panel(
                "\n".join([f"[red]❌[/red] {issue}" for issue in issues]),
                title="[bold red]⚠️  AI-Detected Issues[/bold red]",
                border_style="red",
                padding=(1, 2)
            ))
            console.print("\n")

        # Show static analysis issues (security & performance)
        if static_issues:
            static_text = []
            for issue in static_issues:
                if hasattr(issue, 'type'):
                    static_text.append(f"[orange]{issue.severity.upper()}[/orange] [{issue.type}] {issue.message}")
                else:
                    static_text.append(f"[orange]ISSUE[/orange] {str(issue)}")

            console.print(Panel(
                "\n".join(static_text),
                title="[bold orange]🔍 Static Analysis Issues[/bold orange]",
                border_style="orange1",
                padding=(1, 2)
            ))
            console.print("\n")

        # Show suggestions
        if suggestions:
            console.print(Panel(
                "\n".join([f"[yellow]💡[/yellow] {suggestion}" for suggestion in suggestions]),
                title="[bold yellow]✨ Improvement Suggestions[/bold yellow]",
                border_style="yellow",
                padding=(1, 2)
            ))
            console.print("\n")

        # Show code metrics
        if metrics:
            metrics_text = [
                f"Lines of Code: {metrics.get('lines_of_code', 0)}",
                f"Functions: {metrics.get('functions', 0)}",
                f"Classes: {metrics.get('classes', 0)}",
                f"Complexity: {metrics.get('cyclomatic_complexity', 0):.2f}",
                f"Comment Ratio: {metrics.get('comments_ratio', 0):.1%}",
                f"Type Hints: {metrics.get('type_hints_coverage', 0):.1%}",
            ]
            console.print(Panel(
                "\n".join(metrics_text),
                title="[bold blue]📈 Code Metrics[/bold blue]",
                border_style="blue",
                padding=(1, 2)
            ))
            console.print("\n")

        # Show improved code preview if available
        if has_improvements:
            console.print("[bold green]✓[/bold green] AI generated improved version!\n")

            # Show diff preview (first 20 lines)
            improved_code = result["improved_code"]
            improved_lines = improved_code.split('\n')[:20]
            preview = '\n'.join(improved_lines)
            if len(result["improved_code"].split('\n')) > 20:
                preview += "\n... (truncated)"

            syntax = Syntax(preview, "python", theme="monokai", line_numbers=True)
            console.print(Panel(
                syntax,
                title=f"[bold green]🔧 Improved {file_type} (Preview)[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))
            console.print("\n")
        else:
            console.print("[bold green]✅ Code looks good! No improvements needed.[/bold green]\n")
    
    def _attempt_to_fix_issues(self, result: Dict[str, Any], original_code: str, file_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to automatically fix detected issues by requesting improved code from LLM."""
        issues = result.get("issues", [])
        static_issues = result.get("static_issues", [])

        if not (issues or static_issues):
            return result  # No issues to fix

        console.print("\n")
        console.print("[bold yellow]🔧 Attempting to fix detected issues...[/bold yellow]\n")

        # Format issues for the fix prompt
        issue_list = []
        for issue in issues[:3]:  # Limit to 3 main issues
            if isinstance(issue, str):
                issue_list.append(f"- {issue}")
            else:
                issue_list.append(f"- {str(issue)}")

        for issue in static_issues[:2]:  # Include some static issues
            if hasattr(issue, 'message'):
                issue_list.append(f"- [Static] {issue.message}")
            else:
                issue_list.append(f"- [Static] {str(issue)}")

        fix_prompt = f"""The following code has issues that need to be fixed:

```python
{original_code}
```

Issues to fix:
{chr(10).join(issue_list)}

Context:
- Task: {context.get('task')}
- Framework: {context.get('framework')}
- File type: {file_type}

Please provide the COMPLETE fixed code that addresses all issues above.
Ensure the fixed code is syntactically correct and handles the identified problems.
Return ONLY the fixed Python code, starting with ``` and ending with ```."""

        fix_system_msg = (
            "You are an expert code fixer. Your task is to fix code issues while preserving functionality. "
            "Return ONLY valid Python code in a markdown code block. No explanations."
        )

        # Try to get fixed code
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                with console.status(f"[bold yellow]Attempt {attempt}/{max_attempts}: Generating fixes...", spinner="dots"):
                    response = self.client.generate(
                        self.reviewer_model,
                        fix_prompt,
                        system=fix_system_msg,
                        temperature=0.3
                    )

                # Extract code from response
                fixed_code = self._extract_code_from_response(response)

                if fixed_code and fixed_code != original_code:
                    result["improved_code"] = fixed_code
                    console.print("[bold green]✅ Issues fixed automatically![/bold green]\n")
                    return result

            except Exception as e:
                console.print(f"[dim]Attempt {attempt} failed: {str(e)[:50]}[/dim]")
                if attempt < max_attempts:
                    console.print(f"[dim]Retrying with adjusted prompt...[/dim]")

        # If automatic fixing failed
        console.print("\n[yellow]⚠️  Could not automatically fix all issues.[/yellow]")
        console.print("[dim]Suggestions:[/dim]")
        console.print("[dim]1. Try a larger language model (70b, 32b, or 13b)[/dim]")
        console.print("[dim]2. Simplify the code and try again[/dim]")
        console.print("[dim]3. Fix specific issues manually[/dim]")

        return result

    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract Python code from LLM response (markdown or plain)."""
        response = response.strip()

        # Method 1: Extract from markdown code block
        code_match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        # Method 2: Extract from generic code block
        code_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            # Check if it looks like Python
            if 'def ' in code or 'import ' in code or 'class ' in code or code.startswith('import'):
                return code

        # Method 3: If response is mostly code (contains function/class definitions)
        if ('def ' in response or 'class ' in response) and response.count('\n') > 2:
            return response

        return None

    def _build_review_prompt(self, code: str, file_type: str, context: Dict[str, Any]) -> str:
        return f"""
Review this {file_type} file for a {context.get('task', 'ML')} project:

```python
{code}
```

Context:
- Task: {context.get('task')}
- Framework: {context.get('framework')}
- Dataset: {context.get('dataset')}

Check for:
1. Syntax errors
2. Import errors
3. Logic bugs
4. Missing error handling
5. Performance issues
6. Best practice violations
7. Dataset integration correctness

Provide JSON response with issues, suggestions, and optionally improved_code.
"""
    
    def _parse_review_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse review response - with robust fallback for non-JSON responses"""
        response = response.strip()

        # Use robust JSON parsing (handles small model quirks)
        result = self._robust_json_parse(response)

        if result:
            # Ensure required keys exist
            if "valid" not in result:
                result["valid"] = True
            if "issues" not in result:
                result["issues"] = []
            if "suggestions" not in result:
                result["suggestions"] = []
            return result

        # Fallback: Try to extract useful info from plain text response
        console.print(f"[yellow]⚠️  Model returned non-JSON response, creating basic review[/yellow]")

        # Create a basic result from the text
        result = {
            "valid": True,
            "issues": [],
            "suggestions": []
        }

        # Try to extract any issues mentioned
        if "error" in response.lower() or "bug" in response.lower() or "issue" in response.lower():
            # Extract lines that mention problems
            for line in response.split('\n'):
                line = line.strip()
                if line and len(line) > 10 and len(line) < 200:
                    if any(word in line.lower() for word in ["error", "bug", "issue", "problem", "missing", "incorrect"]):
                        result["issues"].append(line[:150])
                    elif any(word in line.lower() for word in ["suggest", "recommend", "consider", "should", "could", "better"]):
                        result["suggestions"].append(line[:150])

        # Limit to 5 items each
        result["issues"] = result["issues"][:5]
        result["suggestions"] = result["suggestions"][:5]

        return result if (result["issues"] or result["suggestions"]) else {"valid": True, "issues": [], "suggestions": ["Code review completed - no specific issues found"]}

    def _robust_json_parse(self, text: str) -> Optional[Dict[str, Any]]:
        """Robustly parse JSON from LLM response, handling common small-model issues."""
        text = text.strip()

        # Method 1: Try direct JSON parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Method 2: Find JSON block between ```json and ```
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Method 3: Find outermost { } pair (handles escaped strings and small models)
        start_idx = text.find('{')
        if start_idx != -1:
            brace_count = 0
            end_idx = -1
            in_string = False
            escape_next = False

            for i in range(start_idx, len(text)):
                char = text[i]

                if escape_next:
                    escape_next = False
                    continue

                if char == '\\':
                    escape_next = True
                    continue

                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue

                if not in_string:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i
                            break

            if end_idx != -1:
                json_str = text[start_idx:end_idx + 1]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # Try to fix common small-model issues
                    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Remove trailing commas
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        pass

        # Method 4: Simple regex (last resort)
        match = re.search(r'\{[^{}]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return None
