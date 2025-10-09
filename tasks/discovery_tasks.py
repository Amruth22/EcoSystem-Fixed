from crewai import Task
from agents.api_discovery_agent import create_api_discovery_agent

agent = create_api_discovery_agent()

discovery_task = Task(
    description="""Discover and catalog all APIs in the enterprise environment.
    
    Focus on:
    1. Scanning local network for active API services on common ports
    2. Analyzing Git repositories for API definitions and specifications
    3. Identifying API endpoints, technologies, and configurations
    4. Cataloging discovered APIs with comprehensive metadata
    5. Detecting potential security concerns during discovery
    
    Use the Network Scanner Tool and Git Repository Analyzer Tool to gather information.""",
    agent=agent,
    expected_output="A structured JSON report listing all discovered APIs with metadata including endpoints, technologies, security concerns, and discovery methods."
)
