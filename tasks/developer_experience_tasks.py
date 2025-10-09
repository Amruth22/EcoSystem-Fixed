from crewai import Task
from agents.developer_experience_agent import create_developer_experience_agent

agent = create_developer_experience_agent()

developer_experience_task = Task(
    description="""Create developer tools and SDKs to enhance API usability.
    
    Focus on:
    1. Generating multi-language SDKs (Python, JavaScript, Java)
    2. Creating code examples and sample applications
    3. Building interactive API explorers
    4. Developing developer onboarding materials
    5. Ensuring SDKs follow best practices and conventions
    
    Make APIs easy to use and integrate for developers.""",
    agent=agent,
    expected_output="Multi-language SDKs with comprehensive documentation, code examples, interactive tools, and developer onboarding guides."
)
