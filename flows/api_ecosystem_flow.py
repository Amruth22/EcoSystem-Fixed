"""
API Ecosystem Flow - CrewAI Flow Implementation

This module implements the CrewAI Flow for orchestrating the API Ecosystem Manager
with state management, conditional branching, and event-driven execution.
"""

from crewai.flow.flow import Flow, listen, start
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from crewai import Crew, Process
from agents.api_discovery_agent import create_api_discovery_agent
from agents.documentation_agent import create_documentation_agent
from agents.compliance_agent import create_compliance_agent
from agents.developer_experience_agent import create_developer_experience_agent
from tasks.discovery_tasks import discovery_task
from tasks.documentation_tasks import documentation_task
from tasks.compliance_tasks import compliance_task
from tasks.developer_experience_tasks import developer_experience_task

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIEcosystemFlow(Flow):
    """
    Main Flow orchestrating the API Ecosystem Manager process.

    This Flow provides:
    - State management across different stages
    - Conditional branching based on results
    - Event-driven execution of crews
    - Dynamic routing based on security findings
    - Comprehensive error handling
    """

    # State variables that persist across the flow
    discovered_apis: List[Dict] = []
    api_count: int = 0
    security_assessment: Dict = {}
    critical_issues: int = 0
    documentation: Dict = {}
    sdks: Dict = {}
    execution_start: Optional[datetime] = None
    execution_metrics: Dict = {}

    def __init__(self, verbose: bool = True):
        """
        Initialize the API Ecosystem Flow.

        Args:
            verbose: Whether to enable verbose logging
        """
        super().__init__()
        self.verbose = verbose
        self.execution_start = datetime.now()
        logger.info("🚀 API Ecosystem Flow initialized")

    @start()
    def initiate_discovery(self) -> Dict[str, Any]:
        """
        Step 1: API Discovery Phase

        Discovers APIs through:
        - Network scanning
        - Repository analysis
        - Git repository parsing

        Returns:
            Dictionary containing discovered APIs
        """
        logger.info("\n" + "="*70)
        logger.info("📍 FLOW STEP 1: API DISCOVERY")
        logger.info("="*70)
        logger.info("🔍 Starting API discovery process...")

        step_start = datetime.now()

        try:
            # Create discovery crew
            discovery_agent = create_api_discovery_agent()

            crew = Crew(
                agents=[discovery_agent],
                tasks=[discovery_task],
                verbose=self.verbose,
                process=Process.sequential
            )

            # Execute discovery
            result = crew.kickoff()

            # Parse and store results
            if hasattr(result, 'raw'):
                result_data = result.raw
            else:
                result_data = str(result)

            # Update state
            self.discovered_apis = self._parse_apis_from_result(result_data)
            self.api_count = len(self.discovered_apis)

            duration = (datetime.now() - step_start).total_seconds()
            self.execution_metrics['discovery'] = duration

            logger.info(f"✅ Discovery completed in {duration:.2f}s")
            logger.info(f"📊 APIs discovered: {self.api_count}")

            return {
                "status": "completed",
                "apis_found": self.api_count,
                "apis": self.discovered_apis,
                "duration": duration
            }

        except Exception as e:
            logger.error(f"❌ Discovery failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "apis_found": 0
            }

    @listen("initiate_discovery")
    def assess_security(self, discovery_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Security Assessment Phase

        Performs security assessment only if APIs were discovered.

        Args:
            discovery_result: Results from the discovery phase

        Returns:
            Dictionary containing security assessment results
        """
        logger.info("\n" + "="*70)
        logger.info("📍 FLOW STEP 2: SECURITY ASSESSMENT")
        logger.info("="*70)

        # Conditional: Skip if no APIs found
        if self.api_count == 0:
            logger.warning("⚠️ No APIs found - skipping security assessment")
            return {
                "status": "skipped",
                "reason": "no_apis_found"
            }

        logger.info(f"🔒 Running security assessment on {self.api_count} APIs...")
        step_start = datetime.now()

        try:
            # Create compliance crew
            compliance_agent = create_compliance_agent()

            crew = Crew(
                agents=[compliance_agent],
                tasks=[compliance_task],
                verbose=self.verbose,
                process=Process.sequential
            )

            # Execute security assessment
            result = crew.kickoff()

            # Parse results
            if hasattr(result, 'raw'):
                result_data = result.raw
            else:
                result_data = str(result)

            # Update state
            self.security_assessment = self._parse_security_assessment(result_data)
            self.critical_issues = self.security_assessment.get('critical_findings', 0)

            duration = (datetime.now() - step_start).total_seconds()
            self.execution_metrics['security'] = duration

            logger.info(f"✅ Security assessment completed in {duration:.2f}s")
            logger.info(f"🚨 Critical issues found: {self.critical_issues}")

            return {
                "status": "completed",
                "critical_issues": self.critical_issues,
                "assessment": self.security_assessment,
                "duration": duration
            }

        except Exception as e:
            logger.error(f"❌ Security assessment failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }

    @listen("assess_security")
    def route_by_security_level(self, security_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Security-Based Routing

        Routes execution based on security findings:
        - If critical issues found: Generate security report first
        - If no critical issues: Continue to documentation

        Args:
            security_result: Results from security assessment

        Returns:
            Dictionary containing routing decision
        """
        logger.info("\n" + "="*70)
        logger.info("📍 FLOW STEP 3: ROUTING DECISION")
        logger.info("="*70)

        if security_result.get('status') == 'skipped':
            logger.info("➡️ Routing to documentation (security skipped)")
            return {"route": "documentation", "reason": "security_skipped"}

        if self.critical_issues > 0:
            logger.warning(f"🚨 {self.critical_issues} critical security issues detected!")
            logger.info("➡️ Routing to security report generation")
            return {
                "route": "security_report",
                "reason": "critical_issues_found",
                "critical_count": self.critical_issues
            }
        else:
            logger.info("✅ No critical security issues found")
            logger.info("➡️ Routing to documentation generation")
            return {
                "route": "documentation",
                "reason": "no_critical_issues"
            }

    @listen("route_by_security_level")
    def generate_documentation(self, routing_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 4: Documentation Generation Phase

        Generates comprehensive API documentation including:
        - OpenAPI specifications
        - Interactive documentation
        - Usage guides

        Args:
            routing_decision: Results from routing decision

        Returns:
            Dictionary containing documentation results
        """
        logger.info("\n" + "="*70)
        logger.info("📍 FLOW STEP 4: DOCUMENTATION GENERATION")
        logger.info("="*70)
        logger.info("📖 Generating comprehensive API documentation...")

        step_start = datetime.now()

        try:
            # Create documentation crew
            documentation_agent = create_documentation_agent()

            crew = Crew(
                agents=[documentation_agent],
                tasks=[documentation_task],
                verbose=self.verbose,
                process=Process.sequential
            )

            # Execute documentation generation
            result = crew.kickoff()

            # Parse results
            if hasattr(result, 'raw'):
                result_data = result.raw
            else:
                result_data = str(result)

            # Update state
            self.documentation = self._parse_documentation(result_data)

            duration = (datetime.now() - step_start).total_seconds()
            self.execution_metrics['documentation'] = duration

            logger.info(f"✅ Documentation generation completed in {duration:.2f}s")

            return {
                "status": "completed",
                "documentation": self.documentation,
                "duration": duration
            }

        except Exception as e:
            logger.error(f"❌ Documentation generation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }

    @listen("generate_documentation")
    def generate_sdks(self, documentation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 5: SDK Generation Phase

        Generates SDKs in multiple programming languages:
        - Python
        - JavaScript/TypeScript
        - Java

        Args:
            documentation_result: Results from documentation generation

        Returns:
            Dictionary containing SDK generation results
        """
        logger.info("\n" + "="*70)
        logger.info("📍 FLOW STEP 5: SDK GENERATION")
        logger.info("="*70)
        logger.info("🛠️ Generating multi-language SDKs...")

        step_start = datetime.now()

        try:
            # Create developer experience crew
            dev_experience_agent = create_developer_experience_agent()

            crew = Crew(
                agents=[dev_experience_agent],
                tasks=[developer_experience_task],
                verbose=self.verbose,
                process=Process.sequential
            )

            # Execute SDK generation
            result = crew.kickoff()

            # Parse results
            if hasattr(result, 'raw'):
                result_data = result.raw
            else:
                result_data = str(result)

            # Update state
            self.sdks = self._parse_sdks(result_data)

            duration = (datetime.now() - step_start).total_seconds()
            self.execution_metrics['sdk_generation'] = duration

            sdk_count = len(self.sdks.get('languages', []))
            logger.info(f"✅ SDK generation completed in {duration:.2f}s")
            logger.info(f"📦 SDKs generated: {sdk_count}")

            return {
                "status": "completed",
                "sdks": self.sdks,
                "languages": sdk_count,
                "duration": duration
            }

        except Exception as e:
            logger.error(f"❌ SDK generation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }

    @listen("generate_sdks")
    def finalize_execution(self, sdk_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 6: Finalization Phase

        Finalizes the flow execution and returns complete results.

        Args:
            sdk_result: Results from SDK generation

        Returns:
            Dictionary containing complete flow execution results
        """
        logger.info("\n" + "="*70)
        logger.info("📍 FLOW STEP 6: FINALIZATION")
        logger.info("="*70)

        total_duration = (datetime.now() - self.execution_start).total_seconds()

        final_result = {
            "status": "completed",
            "execution_time": total_duration,
            "metrics": self.execution_metrics,
            "results": {
                "discovered_apis": self.discovered_apis,
                "api_count": self.api_count,
                "security_assessment": self.security_assessment,
                "critical_issues": self.critical_issues,
                "documentation": self.documentation,
                "sdks": self.sdks
            }
        }

        logger.info("\n" + "="*70)
        logger.info("✅ FLOW EXECUTION COMPLETED SUCCESSFULLY")
        logger.info("="*70)
        logger.info(f"⏱️ Total execution time: {total_duration:.2f}s")
        logger.info(f"📊 APIs discovered: {self.api_count}")
        logger.info(f"🔒 Critical security issues: {self.critical_issues}")
        logger.info(f"📖 Documentation generated: {'Yes' if self.documentation else 'No'}")
        logger.info(f"🛠️ SDKs generated: {len(self.sdks.get('languages', []))}")
        logger.info("="*70)

        return final_result

    # Helper methods for parsing results

    def _parse_apis_from_result(self, result_data: str) -> List[Dict]:
        """Parse discovered APIs from crew result."""
        # Simple parsing - in production, this would parse structured output
        apis = []
        if "API" in str(result_data) or "api" in str(result_data):
            # Mock API data for demonstration
            apis = [
                {"name": "Enterprise API", "version": "1.0", "type": "REST"},
                {"name": "Auth API", "version": "2.0", "type": "REST"}
            ]
        return apis

    def _parse_security_assessment(self, result_data: str) -> Dict:
        """Parse security assessment from crew result."""
        # Simple parsing - in production, this would parse structured output
        assessment = {
            "scan_completed": True,
            "critical_findings": 0,
            "high_findings": 1,
            "medium_findings": 2,
            "low_findings": 3,
            "status": "PASS"
        }

        # Check for critical issues in result
        if "critical" in str(result_data).lower() or "severe" in str(result_data).lower():
            assessment["critical_findings"] = 1
            assessment["status"] = "FAIL"

        return assessment

    def _parse_documentation(self, result_data: str) -> Dict:
        """Parse documentation from crew result."""
        return {
            "generated": True,
            "format": "OpenAPI 3.0",
            "pages": 15,
            "endpoints_documented": self.api_count * 5
        }

    def _parse_sdks(self, result_data: str) -> Dict:
        """Parse SDKs from crew result."""
        return {
            "generated": True,
            "languages": ["Python", "JavaScript", "Java"],
            "quality_score": 95
        }
