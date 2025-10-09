from crewai import Agent
from tools.security_scanner import SecurityScannerTool
from utils.llm_config import get_llm_config

def create_compliance_agent():
    """
    Create the Compliance Agent with centralized LLM configuration.
    
    Returns:
        Configured Agent for security and compliance
    """
    llm = get_llm_config()
    
    security_tool = SecurityScannerTool()
    
    agent = Agent(
        role="Security and Compliance Auditor",
        goal="Ensure APIs meet security, regulatory, and organizational standards",
        backstory="Cybersecurity expert with deep knowledge of API security frameworks and compliance requirements",
        llm=llm,
        tools=[security_tool],
        verbose=True
    )
    
    return agent
