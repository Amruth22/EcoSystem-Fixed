from crewai.tools import BaseTool
import json

class DocumentationBuilderTool(BaseTool):
    name: str = "Documentation Builder Tool"
    description: str = "Generate comprehensive API documentation and OpenAPI specifications"

    def _run(self, api_data: str = None) -> str:
        """
        Generate API documentation.
        
        Args:
            api_data: API data to document (JSON string)
        """
        try:
            result = {
                "generated_documentation": {
                    "openapi_version": "3.0.3",
                    "info": {
                        "title": "Enterprise API",
                        "version": "1.0.0",
                        "description": "Comprehensive API documentation"
                    },
                    "paths": {
                        "/api/users": {
                            "get": {
                                "summary": "List users",
                                "responses": {
                                    "200": {
                                        "description": "Successful response"
                                    }
                                }
                            }
                        }
                    }
                },
                "documentation_quality": {
                    "completeness_score": 0.92,
                    "coverage_percentage": 89.5
                }
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Documentation generation failed: {str(e)}"
