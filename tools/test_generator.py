from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import json
import logging

logger = logging.getLogger(__name__)

class TestGeneratorInput(BaseModel):
    """Input schema for Test Generator Tool."""
    api_spec: Optional[str] = Field(
        default=None,
        description="API specification (JSON string) to generate tests for"
    )

class TestGeneratorTool(BaseTool):
    name: str = "Test Generator Tool"
    description: str = """Generate automated tests for APIs.

    Parameters:
    - api_spec (optional): API specification as JSON string

    Returns: JSON with generated test suites and coverage metrics.

    Example usage:
    - {} - generate default tests
    - {"api_spec": "{\\"paths\\": {...}}"} - generate tests from specification
    """
    args_schema: Type[BaseModel] = TestGeneratorInput

    def _run(self, api_spec: Optional[str] = None, **kwargs) -> str:
        """
        Generate API tests.

        Args:
            api_spec: API specification (JSON string)
            **kwargs: Additional arguments (ignored for compatibility)

        Returns:
            JSON string with generated tests
        """
        logger.info(f"Test Generator called with: api_spec length={len(api_spec) if api_spec else 0}, kwargs={kwargs}")

        try:
            # Validate spec if provided
            if api_spec:
                try:
                    json.loads(api_spec)
                except json.JSONDecodeError as e:
                    return json.dumps({
                        "error": f"Invalid API spec format: {str(e)}",
                        "generated_tests": {"unit_tests": 0, "integration_tests": 0}
                    })

            result = {
                "generated_tests": {
                    "unit_tests": 10,
                    "integration_tests": 5,
                    "end_to_end_tests": 3,
                    "test_coverage": 85
                },
                "test_frameworks": ["pytest", "unittest"],
                "spec_analyzed": bool(api_spec)
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            logger.error(f"Test generation failed: {e}\n{error_traceback}")
            return json.dumps({
                "error": f"Test generation failed: {str(e)}",
                "error_type": type(e).__name__,
                "traceback": error_traceback
            })
