import unittest

from noless.code_validator import CodeValidator


class FakeOllamaClient:
    def __init__(self, models):
        self._models = models

    def list_models(self):
        return self._models


class CodeValidatorTests(unittest.TestCase):
    def test_uses_requested_reviewer_when_available(self):
        client = FakeOllamaClient(["deepseek-coder:6.7b", "mixtral:8x7b"])
        validator = CodeValidator(
            reviewer_model="mixtral:8x7b",
            generation_model="deepseek-coder:6.7b",
            ollama_client=client,
        )
        self.assertEqual("mixtral:8x7b", validator.reviewer_model)

    def test_falls_back_when_requested_missing(self):
        client = FakeOllamaClient(["deepseek-coder:6.7b", "llama3.1:8b"])
        validator = CodeValidator(
            reviewer_model="mixtral:8x7b",
            generation_model="deepseek-coder:6.7b",
            ollama_client=client,
        )
        self.assertEqual("llama3.1:8b", validator.reviewer_model)

    def test_auto_selects_larger_when_unspecified(self):
        client = FakeOllamaClient(["deepseek-coder:6.7b", "mixtral:8x7b"])
        validator = CodeValidator(
            reviewer_model=None,
            generation_model="deepseek-coder:6.7b",
            ollama_client=client,
        )
        self.assertEqual("mixtral:8x7b", validator.reviewer_model)


if __name__ == "__main__":
    unittest.main()
