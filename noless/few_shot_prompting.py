"""Few-shot prompting examples for improved LLM accuracy."""

from typing import Dict, List, Optional


class FewShotExamples:
    """Repository of few-shot examples for different task types."""

    CODE_REVIEW_EXAMPLES = [
        {
            "code": """
def calculate_sum(numbers):
    result = 0
    for i in numbers:
        result = result + i
    return result
""",
            "review": {
                "valid": True,
                "issues": ["Missing type hints on function parameters and return value"],
                "suggestions": [
                    "Use list comprehension or sum() built-in instead of manual loop",
                    "Add comprehensive docstring explaining function purpose",
                    "Consider edge cases like empty lists"
                ],
                "improved_code": """
def calculate_sum(numbers: List[int]) -> int:
    \"\"\"Calculate the sum of a list of numbers.

    Args:
        numbers: List of integers to sum

    Returns:
        The sum of all numbers in the list

    Example:
        >>> calculate_sum([1, 2, 3])
        6
    \"\"\"
    return sum(numbers)
"""
            }
        },
        {
            "code": """
def get_user_data(user_id):
    db = connect_database()
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    result = db.execute(query)
    return result
""",
            "review": {
                "valid": False,
                "issues": [
                    "Critical SQL injection vulnerability - user input not sanitized",
                    "Missing error handling for database connection failures",
                    "No type hints on parameters and return value"
                ],
                "suggestions": [
                    "Use parameterized queries to prevent SQL injection",
                    "Add try-except for database error handling",
                    "Close database connection after use"
                ],
                "improved_code": """
def get_user_data(user_id: int) -> Optional[Dict[str, Any]]:
    \"\"\"Retrieve user data from database safely.

    Args:
        user_id: ID of the user to retrieve

    Returns:
        User data dictionary or None if not found

    Raises:
        DatabaseError: If database connection fails
    \"\"\"
    try:
        db = connect_database()
        result = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return result.fetchone() if result else None
    except DatabaseError as e:
        raise DatabaseError(f"Failed to fetch user {user_id}: {e}")
    finally:
        db.close()
"""
            }
        }
    ]

    MODEL_DEFINITION_EXAMPLES = [
        {
            "description": "Image classification model for MNIST dataset",
            "framework": "pytorch",
            "example": """
import torch
import torch.nn as nn
from typing import Tuple

class MNISTClassifier(nn.Module):
    \"\"\"CNN for MNIST digit classification.\"\"\"

    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
"""
        }
    ]

    TRAINING_SCRIPT_EXAMPLES = [
        {
            "description": "PyTorch training loop with validation",
            "framework": "pytorch",
            "example": """
import torch
from tqdm import tqdm

def train_epoch(model, train_loader, criterion, optimizer, device):
    \"\"\"Train for one epoch.\"\"\"
    model.train()
    total_loss = 0.0

    for batch_idx, (data, target) in enumerate(tqdm(train_loader)):
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)

def validate(model, val_loader, criterion, device):
    \"\"\"Validate model performance.\"\"\"
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in val_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)

            total_loss += loss.item()
            _, predicted = output.max(1)
            correct += predicted.eq(target).sum().item()
            total += target.size(0)

    accuracy = 100. * correct / total
    avg_loss = total_loss / len(val_loader)
    return avg_loss, accuracy
"""
        }
    ]

    @classmethod
    def get_code_review_examples(cls) -> str:
        """Get few-shot examples for code review."""
        examples_text = "Examples of good code reviews:\n\n"
        for i, example in enumerate(cls.CODE_REVIEW_EXAMPLES, 1):
            examples_text += f"Example {i}:\n"
            examples_text += f"Code:\n{example['code']}\n"
            examples_text += f"Review format (JSON):\n"
            examples_text += f"{{\n"
            examples_text += f'  "valid": {str(example["review"]["valid"]).lower()},\n'
            examples_text += f'  "issues": {example["review"]["issues"]},\n'
            examples_text += f'  "suggestions": {example["review"]["suggestions"]}\n'
            examples_text += f"}}\n\n"
        return examples_text

    @classmethod
    def get_model_examples(cls) -> str:
        """Get few-shot examples for model definition."""
        examples_text = "Examples of good model definitions:\n\n"
        for i, example in enumerate(cls.MODEL_DEFINITION_EXAMPLES, 1):
            examples_text += f"Example {i}: {example['description']}\n"
            examples_text += f"Framework: {example['framework']}\n"
            examples_text += f"Code:\n{example['example']}\n\n"
        return examples_text

    @classmethod
    def get_training_examples(cls) -> str:
        """Get few-shot examples for training scripts."""
        examples_text = "Examples of good training loops:\n\n"
        for i, example in enumerate(cls.TRAINING_SCRIPT_EXAMPLES, 1):
            examples_text += f"Example {i}: {example['description']}\n"
            examples_text += f"Framework: {example['framework']}\n"
            examples_text += f"Code:\n{example['example']}\n\n"
        return examples_text


class ChainOfThoughtPrompting:
    """Implements chain-of-thought prompting for better reasoning."""

    REASONING_TEMPLATE = """
Think through this step-by-step:

1. **Understand**: What is the code trying to do?
2. **Analyze**: What are the potential issues?
3. **Identify**: Which issues are critical vs minor?
4. **Suggest**: What improvements would help?
5. **Provide**: Generate improved code if needed

Now provide your analysis in JSON format with issues, suggestions, and improved_code.
"""

    VALIDATION_TEMPLATE = """
Validate this code thoroughly:

1. **Syntax & Imports**: Check for syntax errors and missing imports
2. **Logic**: Is the logic correct and does it match the intent?
3. **Performance**: Are there inefficient patterns?
4. **Security**: Are there security vulnerabilities?
5. **Style**: Does it follow best practices?

For each category, list specific findings.
"""

    @classmethod
    def enhance_prompt(cls, original_prompt: str, thinking_type: str = "general") -> str:
        """
        Enhance a prompt with chain-of-thought reasoning.

        Args:
            original_prompt: Original prompt to enhance
            thinking_type: Type of thinking (general, validation, reasoning)

        Returns:
            Enhanced prompt with chain-of-thought steps
        """
        if thinking_type == "validation":
            template = cls.VALIDATION_TEMPLATE
        elif thinking_type == "reasoning":
            template = cls.REASONING_TEMPLATE
        else:
            template = cls.REASONING_TEMPLATE

        return f"""{template}

Original task:
{original_prompt}

Remember to think through each step before providing your final answer.
"""

    @classmethod
    def create_step_by_step_prompt(cls, code: str, task: str) -> str:
        """Create a step-by-step analysis prompt."""
        return f"""
Analyze this code step-by-step:

{code}

Task: {task}

Please provide:
1. Initial Assessment (what the code does)
2. Detailed Analysis (line-by-line review)
3. Issues Found (with severity)
4. Recommendations (improvements)
5. Improved Code (if applicable)

Format your response as JSON with these exact keys.
"""


class PromptEnhancer:
    """Enhances prompts with few-shot examples and chain-of-thought."""

    def __init__(self, use_few_shot: bool = True, use_cot: bool = True):
        """
        Initialize prompt enhancer.

        Args:
            use_few_shot: Whether to include few-shot examples
            use_cot: Whether to use chain-of-thought prompting
        """
        self.use_few_shot = use_few_shot
        self.use_cot = use_cot

    def enhance_review_prompt(self, code: str, file_type: str, context: Dict) -> str:
        """
        Enhance a code review prompt.

        Args:
            code: Code to review
            file_type: Type of file (model.py, train.py, etc)
            context: Additional context

        Returns:
            Enhanced prompt
        """
        base_prompt = f"""Review this {file_type} file for a {context.get('task', 'ML')} project:

```python
{code}
```

Context:
- Task: {context.get('task')}
- Framework: {context.get('framework')}
- Dataset: {context.get('dataset')}

Provide JSON with: valid (bool), issues (array), suggestions (array), improved_code (string).
"""

        # Add few-shot examples
        if self.use_few_shot:
            base_prompt = FewShotExamples.get_code_review_examples() + base_prompt

        # Add chain-of-thought
        if self.use_cot:
            base_prompt = ChainOfThoughtPrompting.enhance_prompt(base_prompt, "validation")

        return base_prompt

    def enhance_generation_prompt(self, task: str, framework: str, dataset: str) -> str:
        """
        Enhance a code generation prompt.

        Args:
            task: ML task type
            framework: ML framework
            dataset: Dataset name

        Returns:
            Enhanced prompt with examples
        """
        base_prompt = f"""Generate a {framework} model for {task} on {dataset} dataset.

Include:
1. Proper imports
2. Type hints
3. Docstrings
4. Error handling
5. Configuration comments
"""

        if self.use_few_shot:
            base_prompt = FewShotExamples.get_model_examples() + base_prompt

        return base_prompt
