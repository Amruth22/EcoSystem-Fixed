import logging
from dotenv import load_dotenv
from crew import APIEcosystemCrew
from utils.output_handler import process_and_save_results

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main execution function - Entry point for the application.
    
    This is the primary entry point that orchestrates the entire pipeline:
    1. Initialize the crew orchestrator
    2. Execute the full pipeline
    3. Process and save results
    """
    try:
        logger.info("=" * 70)
        logger.info("Enterprise API Ecosystem Manager")
        logger.info("=" * 70)
        
        # Initialize crew orchestrator
        crew_orchestrator = APIEcosystemCrew(verbose=True)
        
        # Display available workflows
        logger.info("\nAvailable workflows:")
        logger.info("  - run_full_pipeline(): Complete pipeline with all agents")
        logger.info("  - run_discovery_to_docs_pipeline(): Discovery and documentation")
        logger.info("  - run_compliance_check(): Discovery and compliance")
        logger.info("  - run_custom_workflow(): Custom agent selection")
        logger.info("")
        
        # Execute the full pipeline
        logger.info("Starting full API ecosystem pipeline...")
        result = crew_orchestrator.run_full_pipeline()
        
        logger.info("\n" + "=" * 70)
        logger.info("Pipeline execution completed!")
        logger.info("=" * 70)
        
        # Process and save all results
        if process_and_save_results(result):
            logger.info("\n" + "=" * 70)
            logger.info("SUCCESS: Pipeline completed successfully!")
            logger.info("All outputs saved to 'outputs' directory")
            logger.info("=" * 70)
        else:
            logger.error("Failed to process and save results")
        
    except Exception as e:
        logger.error(f"\nERROR: Pipeline failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
