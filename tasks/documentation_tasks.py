from crewai import Task
from agents.documentation_agent import create_documentation_agent

agent = create_documentation_agent()

documentation_task = Task(
    description="""Generate comprehensive API documentation for all discovered APIs.
    
    Focus on:
    1. Creating OpenAPI 3.0 specifications for each API
    2. Generating interactive API documentation
    3. Writing clear endpoint descriptions with examples
    4. Documenting authentication and authorization methods
    5. Creating developer guides and tutorials
    
    Ensure documentation is clear, accurate, and developer-friendly.""",
    agent=agent,
    expected_output="Complete API documentation including OpenAPI specifications, interactive docs, code examples, and developer guides in Markdown format."
)
