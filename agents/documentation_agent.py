from crewai import Agent
from utils.llm_config import get_llm_config

def create_documentation_agent():
    """
    Create the Documentation Agent with centralized LLM configuration.
    
    Returns:
        Configured Agent for documentation generation
    """
    llm = get_llm_config()
    
    agent = Agent(
        role="Technical Documentation Expert",
        goal="Generate comprehensive, accurate API documentation automatically",
        backstory="Technical writer with expertise in API specifications and developer experience",
        llm=llm,
        verbose=True
    )
    
    return agent
