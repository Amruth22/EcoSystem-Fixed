from crewai import Agent
from utils.llm_config import get_llm_config

def create_developer_experience_agent():
    """
    Create the Developer Experience Agent with centralized LLM configuration.
    
    Returns:
        Configured Agent for developer experience optimization
    """
    llm = get_llm_config()
    
    agent = Agent(
        role="Developer Experience Optimizer",
        goal="Create exceptional developer experiences through SDKs, tools, and documentation",
        backstory="Developer advocate with expertise in SDK design and developer tooling",
        llm=llm,
        verbose=True
    )
    
    return agent
