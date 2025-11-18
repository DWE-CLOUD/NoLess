"""Pydantic schemas for type-safe validation across NoLess components."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, validator


class CodeIssue(BaseModel):
    """Represents a code issue found during validation."""

    severity: str = Field(..., description="Issue severity: error, warning, info")
    message: str = Field(..., description="Detailed issue description")
    line: Optional[int] = Field(None, description="Line number where issue occurs")
    category: str = Field(..., description="Category: syntax, logic, performance, security, style")
    suggestion: Optional[str] = Field(None, description="Suggested fix")


class CodeSuggestion(BaseModel):
    """Represents a suggestion for code improvement."""

    title: str = Field(..., description="Short title of the suggestion")
    description: str = Field(..., description="Detailed description")
    type: str = Field(..., description="Type: optimization, refactoring, best-practice, testing")
    priority: str = Field(default="medium", description="Priority: low, medium, high")


class CodeReviewResult(BaseModel):
    """Validated response from code review."""

    valid: bool = Field(default=True, description="Whether code is valid")
    issues: List[CodeIssue] = Field(default_factory=list, description="Issues found")
    suggestions: List[CodeSuggestion] = Field(default_factory=list, description="Improvement suggestions")
    improved_code: Optional[str] = Field(None, description="AI-improved version of the code")
    summary: str = Field(default="", description="Summary of the review")

    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "issues": [
                    {
                        "severity": "warning",
                        "message": "Missing error handling",
                        "line": 42,
                        "category": "error-handling",
                        "suggestion": "Wrap in try-except block"
                    }
                ],
                "suggestions": [
                    {
                        "title": "Add type hints",
                        "description": "Function parameters lack type hints",
                        "type": "best-practice",
                        "priority": "medium"
                    }
                ],
                "improved_code": None,
                "summary": "Code has 1 warning and 1 suggestion"
            }
        }


class DatasetMetadata(BaseModel):
    """Metadata about a dataset."""

    name: str = Field(..., description="Dataset name")
    source: str = Field(..., description="Source: huggingface, kaggle, uci, openml")
    url: Optional[str] = Field(None, description="Dataset URL")
    size: Optional[str] = Field(None, description="Dataset size")
    description: Optional[str] = Field(None, description="Dataset description")
    features: Optional[int] = Field(None, description="Number of features")
    samples: Optional[int] = Field(None, description="Number of samples")
    task_type: Optional[str] = Field(None, description="ML task type: classification, regression, clustering")
    license: Optional[str] = Field(None, description="Dataset license")
    columns: Optional[List[str]] = Field(None, description="Column names")


class AutopilotPlanData(BaseModel):
    """Validated autopilot plan."""

    task: str = Field(..., description="ML task type")
    framework: str = Field(..., description="ML framework: pytorch, tensorflow, sklearn")
    dataset_query: str = Field(..., description="Dataset search query")
    architecture: Optional[str] = Field(None, description="Model architecture recommendation")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Recommended hyperparameters")
    notes: str = Field(default="", description="Additional notes")
    confidence: float = Field(default=0.8, description="Confidence score 0-1")


class CodeMetrics(BaseModel):
    """Code quality metrics."""

    lines_of_code: int = Field(..., description="Total lines of code")
    cyclomatic_complexity: float = Field(..., description="Average cyclomatic complexity")
    functions: int = Field(..., description="Number of functions")
    classes: int = Field(..., description="Number of classes")
    comments_ratio: float = Field(..., description="Comment to code ratio (0-1)")
    duplicated_lines: int = Field(default=0, description="Number of duplicated lines")
    type_hints_coverage: float = Field(default=0.0, description="Type hints coverage (0-1)")


class SecurityIssue(BaseModel):
    """Security vulnerability found in code."""

    type: str = Field(..., description="Vulnerability type: injection, hardcoded-secret, weak-crypto, etc")
    severity: str = Field(..., description="Severity: low, medium, high, critical")
    message: str = Field(..., description="Detailed message")
    line: Optional[int] = Field(None, description="Line number")
    fix: Optional[str] = Field(None, description="Suggested fix")


class PerformanceIssue(BaseModel):
    """Performance problem identified in code."""

    type: str = Field(..., description="Issue type: inefficient-loop, memory-leak, unnecessary-copy, etc")
    location: Optional[str] = Field(None, description="Function/line where issue occurs")
    message: str = Field(..., description="Description of the issue")
    impact: str = Field(default="medium", description="Performance impact: low, medium, high")
    suggestion: Optional[str] = Field(None, description="How to optimize")


class ProjectGenerationResult(BaseModel):
    """Result of project generation."""

    success: bool = Field(..., description="Whether generation succeeded")
    project_dir: str = Field(..., description="Generated project directory")
    files_created: List[str] = Field(default_factory=list, description="List of created files")
    validation_results: Optional[Dict[str, CodeReviewResult]] = Field(None, description="Validation results per file")
    warnings: List[str] = Field(default_factory=list, description="Non-critical warnings")
    errors: List[str] = Field(default_factory=list, description="Errors that occurred")


class LLMResponse(BaseModel):
    """Validated LLM response with optional JSON content."""

    raw: str = Field(..., description="Raw LLM response text")
    json_content: Optional[Dict[str, Any]] = Field(None, description="Extracted JSON if present")
    is_valid_json: bool = Field(default=False, description="Whether response contains valid JSON")
    parsing_error: Optional[str] = Field(None, description="Error if JSON parsing failed")
