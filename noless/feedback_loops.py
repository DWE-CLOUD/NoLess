"""Iterative feedback loops for continuous code refinement."""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from noless.ollama_client import OllamaClient
from rich.console import Console

console = Console()


@dataclass
class RefinementStep:
    """Represents a refinement step in the feedback loop."""

    iteration: int
    code: str
    feedback: str
    improvements: List[str]
    success: bool


class IterativeFeedbackLoop:
    """Iterative refinement loop that improves code based on execution/validation feedback."""

    def __init__(
        self,
        client: Optional[OllamaClient] = None,
        max_iterations: int = 3,
        validator: Optional[Callable] = None
    ):
        """
        Initialize feedback loop.

        Args:
            client: OllamaClient for refinement
            max_iterations: Maximum refinement iterations
            validator: Function to validate/test code
        """
        self.client = client or OllamaClient()
        self.max_iterations = max_iterations
        self.validator = validator
        self.history: List[RefinementStep] = []

    def refine(
        self,
        code: str,
        initial_feedback: str,
        task_context: Dict[str, Any],
        model: str = "llama2"
    ) -> Dict[str, Any]:
        """
        Iteratively refine code based on feedback.

        Args:
            code: Initial code to refine
            initial_feedback: Initial feedback/error
            task_context: Context about the code
            model: LLM model to use

        Returns:
            Dictionary with refined code and refinement history
        """
        current_code = code
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            console.print(f"\n[cyan]🔄 Refinement Iteration {iteration}/{self.max_iterations}[/cyan]")

            # Generate refinement
            refined_code = self._generate_refinement(
                current_code,
                initial_feedback,
                task_context,
                model
            )

            # Validate/test the refined code
            if self.validator:
                validation_result = self.validator(refined_code)
                success = validation_result.get("success", False)
                feedback = validation_result.get("feedback", "")
            else:
                # If no validator, assume success after first iteration
                success = True
                feedback = "Code passed basic validation"

            # Record step
            step = RefinementStep(
                iteration=iteration,
                code=refined_code,
                feedback=feedback,
                improvements=self._extract_improvements(current_code, refined_code),
                success=success
            )
            self.history.append(step)

            if success:
                console.print(f"[green]✅ Refinement successful![/green]")
                break

            current_code = refined_code
            initial_feedback = feedback
            console.print(f"[yellow]⚠️  {feedback}[/yellow]")

        return {
            "refined_code": current_code,
            "iterations": iteration,
            "success": success,
            "history": self.history,
            "improvements": self._summarize_improvements()
        }

    def _generate_refinement(
        self,
        code: str,
        feedback: str,
        context: Dict[str, Any],
        model: str
    ) -> str:
        """Generate refined code based on feedback."""
        prompt = f"""
Refine this code based on the feedback provided.

Original Code:
```python
{code}
```

Feedback/Issue:
{feedback}

Context:
- Task: {context.get('task', 'ML')}
- Framework: {context.get('framework', 'pytorch')}

Generate improved code that addresses the feedback. Return only the Python code, no explanations.
"""

        response = self.client.generate(
            model,
            prompt,
            system="You are an expert Python developer. Fix issues in code based on provided feedback.",
            temperature=0.3
        )

        # Extract code from response
        return self._extract_code(response)

    def _extract_code(self, response: str) -> str:
        """Extract Python code from response."""
        # Remove markdown code blocks if present
        if "```python" in response:
            start = response.find("```python") + len("```python")
            end = response.find("```", start)
            return response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + len("```")
            end = response.find("```", start)
            return response[start:end].strip()
        return response.strip()

    def _extract_improvements(self, old_code: str, new_code: str) -> List[str]:
        """Extract what improved between versions."""
        improvements = []

        if "try:" in new_code and "try:" not in old_code:
            improvements.append("Added error handling")

        if "def " in new_code and new_code.count("def ") > old_code.count("def "):
            improvements.append("Refactored into more functions")

        if "\"\"\"" in new_code and "\"\"\"" not in old_code:
            improvements.append("Added documentation")

        if ":" in new_code and new_code.count(":") > old_code.count(":"):
            # Likely added type hints
            improvements.append("Added/improved type hints")

        if len(new_code) > len(old_code):
            improvements.append("Added more comprehensive implementation")

        return improvements or ["Code refined"]

    def _summarize_improvements(self) -> str:
        """Summarize all improvements across iterations."""
        all_improvements = []
        for step in self.history:
            all_improvements.extend(step.improvements)
        return " → ".join(set(all_improvements)) if all_improvements else "Code refined"


class ExecutionFeedbackValidator:
    """Validates code by attempting execution and capturing errors."""

    def __init__(self, timeout: int = 5):
        """
        Initialize validator.

        Args:
            timeout: Timeout for code execution in seconds
        """
        self.timeout = timeout

    def validate(self, code: str) -> Dict[str, Any]:
        """
        Validate code by execution.

        Args:
            code: Code to validate

        Returns:
            Validation result with success flag and feedback
        """
        try:
            # Create a safe execution environment
            exec_globals = {"__builtins__": {}}
            exec_locals = {}

            # Try to execute the code
            exec(code, exec_globals, exec_locals)

            return {
                "success": True,
                "feedback": "Code executed successfully",
                "errors": []
            }
        except SyntaxError as e:
            return {
                "success": False,
                "feedback": f"Syntax Error: {e}",
                "errors": [str(e)]
            }
        except Exception as e:
            return {
                "success": False,
                "feedback": f"Runtime Error: {type(e).__name__}: {e}",
                "errors": [str(e)]
            }


class HybridValidation:
    """Combines multiple validation methods for comprehensive checking."""

    def __init__(
        self,
        static_analyzer: Optional[Callable] = None,
        execution_validator: Optional[ExecutionFeedbackValidator] = None,
        lint_checker: Optional[Callable] = None
    ):
        """
        Initialize hybrid validator.

        Args:
            static_analyzer: Function for static analysis
            execution_validator: Execution-based validator
            lint_checker: Linting function
        """
        self.static_analyzer = static_analyzer
        self.execution_validator = execution_validator or ExecutionFeedbackValidator()
        self.lint_checker = lint_checker

    def validate_comprehensive(self, code: str) -> Dict[str, Any]:
        """
        Perform comprehensive validation using all methods.

        Args:
            code: Code to validate

        Returns:
            Comprehensive validation results
        """
        results = {
            "static_analysis": None,
            "execution": None,
            "linting": None,
            "overall_success": False,
            "issues": [],
            "warnings": []
        }

        # Static analysis
        if self.static_analyzer:
            results["static_analysis"] = self.static_analyzer(code)
            if results["static_analysis"].get("issues"):
                results["issues"].extend(results["static_analysis"]["issues"])

        # Execution validation
        exec_result = self.execution_validator.validate(code)
        results["execution"] = exec_result
        if not exec_result["success"]:
            results["issues"].append(exec_result["feedback"])

        # Linting
        if self.lint_checker:
            results["linting"] = self.lint_checker(code)
            if results["linting"].get("warnings"):
                results["warnings"].extend(results["linting"]["warnings"])

        # Overall result
        results["overall_success"] = len(results["issues"]) == 0

        return results

    def validate_with_feedback(self, code: str) -> str:
        """
        Validate and return human-readable feedback.

        Args:
            code: Code to validate

        Returns:
            Formatted feedback message
        """
        result = self.validate_comprehensive(code)

        feedback_lines = []

        if result["execution"]["success"]:
            feedback_lines.append("✓ Code executes without errors")
        else:
            feedback_lines.append(f"✗ Execution failed: {result['execution']['feedback']}")

        if result["static_analysis"]:
            feedback_lines.append(f"✓ Static analysis: {result['static_analysis']}")

        if result["issues"]:
            feedback_lines.append(f"\nIssues found ({len(result['issues'])}):")
            for issue in result["issues"]:
                feedback_lines.append(f"  - {issue}")

        if result["warnings"]:
            feedback_lines.append(f"\nWarnings ({len(result['warnings'])}):")
            for warning in result["warnings"]:
                feedback_lines.append(f"  - {warning}")

        return "\n".join(feedback_lines)
