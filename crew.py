from crewai import Crew, Process
from typing import Any, Optional, List
import logging
from datetime import datetime

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


class APIEcosystemCrew:
    """
    Main crew orchestration class for the API Ecosystem Manager.
    
    This class encapsulates all crew-related logic and provides a clean
    interface for running different workflows.
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the crew orchestrator.
        
        Args:
            verbose: Whether to enable verbose output during execution
        """
        self.verbose = verbose
        self.agents = {}
        self.tasks = {}
        self._initialize_agents()
        self._initialize_tasks()
        logger.info("API Ecosystem Crew initialized successfully")
    
    def _initialize_agents(self):
        """Initialize all agents for the crew."""
        logger.info("Initializing agents...")
        
        self.agents = {
            'discovery': create_api_discovery_agent(),
            'documentation': create_documentation_agent(),
            'compliance': create_compliance_agent(),
            'developer_experience': create_developer_experience_agent()
        }
        
        logger.info(f"Initialized {len(self.agents)} agents")
    
    def _initialize_tasks(self):
        """Initialize all tasks for the crew."""
        logger.info("Initializing tasks...")
        
        self.tasks = {
            'discovery': discovery_task,
            'documentation': documentation_task,
            'compliance': compliance_task,
            'developer_experience': developer_experience_task
        }
        
        logger.info(f"Initialized {len(self.tasks)} tasks")
    
    def create_crew(
        self,
        agents: Optional[List[str]] = None,
        tasks: Optional[List[str]] = None,
        process: Process = Process.sequential
    ) -> Crew:
        """
        Create a crew with specified agents and tasks.
        
        Args:
            agents: List of agent keys to include (default: all agents)
            tasks: List of task keys to include (default: all tasks)
            process: CrewAI process type (sequential or hierarchical)
        
        Returns:
            Configured Crew instance
        """
        agent_keys = agents or list(self.agents.keys())
        task_keys = tasks or list(self.tasks.keys())
        
        selected_agents = [self.agents[key] for key in agent_keys if key in self.agents]
        selected_tasks = [self.tasks[key] for key in task_keys if key in self.tasks]
        
        logger.info(f"Creating crew with {len(selected_agents)} agents and {len(selected_tasks)} tasks")
        
        crew = Crew(
            agents=selected_agents,
            tasks=selected_tasks,
            verbose=self.verbose,
            process=process
        )
        
        return crew
    
    def run_full_pipeline(self) -> Any:
        """
        Run the complete API ecosystem management pipeline.
        
        This is the main workflow that includes all agents and tasks.
        
        Returns:
            The result of the crew execution
        """
        logger.info("Starting full API ecosystem pipeline...")
        start_time = datetime.now()
        
        crew = self.create_crew()
        result = crew.kickoff()
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Full pipeline completed in {duration:.2f} seconds")
        
        return result
    
    def run_discovery_to_docs_pipeline(self) -> Any:
        """
        Run a streamlined pipeline from discovery to documentation.
        
        This workflow focuses on discovery and documentation only.
        
        Returns:
            The result of the crew execution
        """
        logger.info("Starting discovery-to-documentation pipeline...")
        start_time = datetime.now()
        
        crew = self.create_crew(
            agents=['discovery', 'documentation'],
            tasks=['discovery', 'documentation']
        )
        
        result = crew.kickoff()
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Discovery-to-docs pipeline completed in {duration:.2f} seconds")
        
        return result
    
    def run_compliance_check(self) -> Any:
        """
        Run a compliance-focused workflow.
        
        This workflow focuses on security and compliance checking.
        
        Returns:
            The result of the crew execution
        """
        logger.info("Starting compliance check workflow...")
        start_time = datetime.now()
        
        crew = self.create_crew(
            agents=['discovery', 'compliance'],
            tasks=['discovery', 'compliance']
        )
        
        result = crew.kickoff()
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Compliance check completed in {duration:.2f} seconds")
        
        return result
    
    def run_custom_workflow(
        self,
        agents: List[str],
        tasks: List[str],
        process: Process = Process.sequential
    ) -> Any:
        """
        Run a custom workflow with specified agents and tasks.
        
        Args:
            agents: List of agent keys to include
            tasks: List of task keys to include
            process: CrewAI process type
        
        Returns:
            The result of the crew execution
        """
        logger.info(f"Starting custom workflow with agents: {agents}, tasks: {tasks}")
        start_time = datetime.now()
        
        crew = self.create_crew(agents=agents, tasks=tasks, process=process)
        result = crew.kickoff()
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Custom workflow completed in {duration:.2f} seconds")
        
        return result
    
    def get_agent(self, agent_key: str):
        """Get a specific agent by key."""
        return self.agents.get(agent_key)
    
    def get_task(self, task_key: str):
        """Get a specific task by key."""
        return self.tasks.get(task_key)
    
    def list_available_agents(self) -> List[str]:
        """Get list of available agent keys."""
        return list(self.agents.keys())
    
    def list_available_tasks(self) -> List[str]:
        """Get list of available task keys."""
        return list(self.tasks.keys())


def create_api_ecosystem_crew(verbose: bool = True) -> APIEcosystemCrew:
    """
    Create and return an API Ecosystem Crew instance.
    
    Args:
        verbose: Whether to enable verbose output
    
    Returns:
        APIEcosystemCrew instance
    """
    return APIEcosystemCrew(verbose=verbose)


def run_full_pipeline(verbose: bool = True) -> Any:
    """
    Quick function to run the full pipeline.
    
    Args:
        verbose: Whether to enable verbose output
    
    Returns:
        The result of the crew execution
    """
    crew_orchestrator = APIEcosystemCrew(verbose=verbose)
    return crew_orchestrator.run_full_pipeline()
