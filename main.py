import logging
import os
from dotenv import load_dotenv
from flows.api_ecosystem_flow import APIEcosystemFlow
from utils.output_handler import process_and_save_results

load_dotenv()

# Disable CrewAI telemetry to prevent connection errors
os.environ['OTEL_SDK_DISABLED'] = 'true'
os.environ['DO_NOT_TRACK'] = '1'

# Suppress CrewAI telemetry logging
logging.getLogger('crewai.telemetry.telemetry').setLevel(logging.CRITICAL)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main execution function - Entry point for the application.

    This is the primary entry point that orchestrates the entire pipeline using CrewAI Flow:
    1. Initialize the Flow orchestrator
    2. Execute the Flow with state management and conditional branching
    3. Process and save results

    The Flow provides:
    - State management across different stages
    - Conditional branching based on results
    - Event-driven execution of crews
    - Dynamic routing based on security findings
    """
    try:
        logger.info("=" * 70)
        logger.info("Enterprise API Ecosystem Manager with CrewAI Flow")
        logger.info("=" * 70)

        logger.info("\n🌊 Flow Architecture:")
        logger.info("  1. API Discovery → Discovers APIs via network scanning and repo analysis")
        logger.info("  2. Security Assessment → Conditional: Runs only if APIs found")
        logger.info("  3. Security Routing → Conditional: Routes based on critical issues")
        logger.info("  4. Documentation Generation → Generates comprehensive API docs")
        logger.info("  5. SDK Generation → Creates multi-language SDKs")
        logger.info("  6. Finalization → Aggregates results and metrics")
        logger.info("")

        # Initialize and execute Flow
        logger.info("🚀 Starting API Ecosystem Flow...")
        flow = APIEcosystemFlow(verbose=True)

        # Execute the flow - this runs all steps with state management
        result = flow.kickoff()

        logger.info("\n" + "=" * 70)
        logger.info("Flow execution completed!")
        logger.info("=" * 70)

        # Process and save all results
        if process_and_save_results(result):
            logger.info("\n" + "=" * 70)
            logger.info("SUCCESS: Flow completed successfully!")
            logger.info("All outputs saved to 'outputs' directory")
            logger.info("=" * 70)

            # Display flow metrics
            if 'metrics' in result:
                logger.info("\n📊 Flow Execution Metrics:")
                for step, duration in result['metrics'].items():
                    logger.info(f"  - {step}: {duration:.2f}s")
                logger.info(f"  - Total: {result.get('execution_time', 0):.2f}s")
        else:
            logger.warning("⚠️ Failed to process and save results (non-critical)")

        return result

    except Exception as e:
        logger.error(f"\n❌ ERROR: Flow execution failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
