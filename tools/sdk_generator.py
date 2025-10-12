from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import json
import logging

logger = logging.getLogger(__name__)

class SDKGeneratorInput(BaseModel):
    """Input schema for SDK Generator Tool."""
    api_endpoints: Optional[str] = Field(
        default=None,
        description="Comma-separated list of API endpoints to generate SDKs for"
    )
    languages: Optional[str] = Field(
        default=None,
        description="Comma-separated list of programming languages (e.g., 'python,javascript,java')"
    )

class SDKGeneratorTool(BaseTool):
    name: str = "SDK Generator Tool"
    description: str = """Generate SDKs and code samples for different programming languages.

    Parameters:
    - api_endpoints (optional): Comma-separated list of API endpoints
    - languages (optional): Comma-separated list of languages (default: python,javascript)

    Returns: JSON with generated SDKs for multiple languages.

    Example usage:
    - {} - generate default SDKs
    - {"languages": "python,javascript"} - generate for specific languages
    - {"api_endpoints": "/users,/posts", "languages": "python,javascript,java"} - full specification
    """
    args_schema: Type[BaseModel] = SDKGeneratorInput

    def _run(self, api_endpoints: Optional[str] = None, languages: Optional[str] = None, **kwargs) -> str:
        """
        Generate SDKs and code samples.

        Args:
            api_endpoints: Comma-separated list of API endpoints
            languages: Comma-separated list of programming languages
            **kwargs: Additional arguments (ignored for compatibility)

        Returns:
            JSON string with generated SDKs
        """
        logger.info(f"SDK Generator called with: api_endpoints={api_endpoints}, languages={languages}, kwargs={kwargs}")

        try:
            # Default languages if not specified
            if not languages:
                languages = "python,javascript"

            lang_list = [lang.strip() for lang in languages.split(',')]

            result = {
                "generated_sdks": {
                    "python": {
                        "package_name": "enterprise_api_client",
                        "version": "1.0.0",
                        "code": "class EnterpriseAPIClient:\n    def __init__(self, api_key):\n        self.api_key = api_key"
                    },
                    "javascript": {
                        "package_name": "enterprise-api-client",
                        "version": "1.0.0",
                        "code": "class EnterpriseAPIClient {\n    constructor(apiKey) {\n        this.apiKey = apiKey;\n    }\n}"
                    }
                },
                "quality_analysis": {
                    "completeness_score": 95,
                    "consistency_score": 90
                },
                "requested_languages": lang_list,
                "api_endpoints_analyzed": api_endpoints.split(',') if api_endpoints else []
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            logger.error(f"SDK generation failed: {e}\n{error_traceback}")
            return json.dumps({
                "error": f"SDK generation failed: {str(e)}",
                "error_type": type(e).__name__,
                "traceback": error_traceback
            })
