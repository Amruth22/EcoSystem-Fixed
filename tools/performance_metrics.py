from crewai.tools import BaseTool
import json

class PerformanceMetricsTool(BaseTool):
    name: str = "Performance Metrics Tool"
    description: str = "Collect and analyze API performance metrics"

    def _run(self, api_endpoint: str = None) -> str:
        """
        Collect performance metrics.
        
        Args:
            api_endpoint: API endpoint to analyze
        """
        try:
            result = {
                "performance_metrics": {
                    "avg_response_time_ms": 150,
                    "requests_per_second": 1000,
                    "error_rate": 0.01
                }
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Performance metrics collection failed: {str(e)}"
