from crewai import Agent
from tools.git_analyzer import GitRepositoryAnalyzerTool
from tools.network_scanner import NetworkScannerTool
from utils.llm_config import get_llm_config

def create_api_discovery_agent():
    """
    Create the API Discovery Agent with centralized LLM configuration.
    
    Returns:
        Configured Agent for API discovery
    """
    llm = get_llm_config()
    
    git_tool = GitRepositoryAnalyzerTool()
    network_tool = NetworkScannerTool()
    
    agent = Agent(
        role="API Discovery Specialist",
        goal="Continuously discover and catalog all APIs across the enterprise",
        backstory="Expert system administrator with deep knowledge of network protocols and API architectures",
        llm=llm,
        tools=[git_tool, network_tool],
        verbose=True
    )
    
    return agent
