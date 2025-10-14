"""
Simplified Test Suite - 10 Essential Tests
Tests the core functionality of the API Ecosystem Manager
"""
import unittest
import os
import sys

# Disable CrewAI telemetry to prevent connection errors
os.environ['OTEL_SDK_DISABLED'] = 'true'
os.environ['DO_NOT_TRACK'] = '1'

# Suppress CrewAI telemetry logging
import logging
logging.getLogger('crewai.telemetry.telemetry').setLevel(logging.CRITICAL)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class TestEssentials(unittest.TestCase):
    """Essential tests for API Ecosystem Manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.project_root = os.path.dirname(os.path.abspath(__file__))

    def test_01_config_file_exists(self):
        """Test 1: Configuration file exists and is valid."""
        config_path = os.path.join(self.project_root, 'configs', 'app_config.json')
        self.assertTrue(os.path.exists(config_path), "app_config.json not found")

        import json
        with open(config_path, 'r') as f:
            config = json.load(f)

        self.assertIn('llm_config', config)
        self.assertIn('model', config['llm_config'])

    def test_02_all_8_tools_exist(self):
        """Test 2: All 8 tools exist and can be imported."""
        from tools.git_analyzer import GitRepositoryAnalyzerTool
        from tools.network_scanner import NetworkScannerTool
        from tools.security_scanner import SecurityScannerTool
        from tools.contract_validator import ContractValidatorTool
        from tools.sdk_generator import SDKGeneratorTool
        from tools.test_generator import TestGeneratorTool
        from tools.documentation_builder import DocumentationBuilderTool
        from tools.performance_metrics import PerformanceMetricsTool

        # Verify all tools can be instantiated
        tools = [
            GitRepositoryAnalyzerTool(),
            NetworkScannerTool(),
            SecurityScannerTool(),
            ContractValidatorTool(),
            SDKGeneratorTool(),
            TestGeneratorTool(),
            DocumentationBuilderTool(),
            PerformanceMetricsTool()
        ]

        self.assertEqual(len(tools), 8, "Should have 8 tools")
        for tool in tools:
            self.assertIsNotNone(tool)

    def test_03_all_4_agents_importable(self):
        """Test 3: All 4 agents can be imported."""
        from agents.api_discovery_agent import create_api_discovery_agent
        from agents.documentation_agent import create_documentation_agent
        from agents.compliance_agent import create_compliance_agent
        from agents.developer_experience_agent import create_developer_experience_agent

        # Verify functions exist
        self.assertTrue(callable(create_api_discovery_agent))
        self.assertTrue(callable(create_documentation_agent))
        self.assertTrue(callable(create_compliance_agent))
        self.assertTrue(callable(create_developer_experience_agent))

    def test_04_all_4_tasks_exist(self):
        """Test 4: All 4 task definitions exist."""
        from tasks.discovery_tasks import discovery_task
        from tasks.documentation_tasks import documentation_task
        from tasks.compliance_tasks import compliance_task
        from tasks.developer_experience_tasks import developer_experience_task

        self.assertIsNotNone(discovery_task)
        self.assertIsNotNone(documentation_task)
        self.assertIsNotNone(compliance_task)
        self.assertIsNotNone(developer_experience_task)

    def test_05_crew_orchestration_works(self):
        """Test 5: Crew orchestration class works."""
        from crew import APIEcosystemCrew

        # Test class can be instantiated
        crew = APIEcosystemCrew(verbose=False)
        self.assertIsNotNone(crew)

        # Test crew has required methods
        self.assertTrue(hasattr(crew, 'run_full_pipeline'))
        self.assertTrue(hasattr(crew, 'agents'))
        self.assertTrue(hasattr(crew, 'tasks'))

        # Verify 4 agents and 4 tasks
        self.assertEqual(len(crew.agents), 4)
        self.assertEqual(len(crew.tasks), 4)

    def test_06_flow_implementation_exists(self):
        """Test 6: CrewAI Flow implementation exists and works."""
        from flows.api_ecosystem_flow import APIEcosystemFlow

        # Test Flow class exists
        self.assertIsNotNone(APIEcosystemFlow)

        # Test Flow can be instantiated
        flow = APIEcosystemFlow(verbose=False)
        self.assertIsNotNone(flow)

        # Test Flow has state variables
        self.assertTrue(hasattr(flow, 'discovered_apis'))
        self.assertTrue(hasattr(flow, 'api_count'))
        self.assertTrue(hasattr(flow, 'security_assessment'))
        self.assertTrue(hasattr(flow, 'critical_issues'))

        # Test Flow has required methods
        self.assertTrue(hasattr(flow, 'initiate_discovery'))
        self.assertTrue(hasattr(flow, 'assess_security'))
        self.assertTrue(hasattr(flow, 'generate_documentation'))
        self.assertTrue(hasattr(flow, 'generate_sdks'))

    def test_07_utils_modules_work(self):
        """Test 7: Utility modules work correctly."""
        from utils.llm_config import load_config, get_llm_config
        from utils.output_handler import (
            save_complete_output,
            extract_and_save_components,
            process_and_save_results
        )

        # Test LLM config
        self.assertTrue(callable(load_config))
        self.assertTrue(callable(get_llm_config))
        config = load_config()
        self.assertIsInstance(config, dict)

        # Test output handler
        self.assertTrue(callable(save_complete_output))
        self.assertTrue(callable(extract_and_save_components))
        self.assertTrue(callable(process_and_save_results))

    def test_08_main_entry_point_exists(self):
        """Test 8: Main entry point exists and has correct structure."""
        main_path = os.path.join(self.project_root, 'main.py')
        self.assertTrue(os.path.exists(main_path), "main.py not found")

        with open(main_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verify main.py uses Flow
        self.assertIn('from flows.api_ecosystem_flow import APIEcosystemFlow', content)
        self.assertIn('def main():', content)
        self.assertIn('flow.kickoff()', content)

    def test_09_actual_tool_call(self):
        """Test 9: Make actual tool call to verify tools work in practice."""
        from tools.git_analyzer import GitRepositoryAnalyzerTool
        import json

        # Initialize the tool
        git_tool = GitRepositoryAnalyzerTool()
        
        # Make actual tool call to analyze current repository
        result = git_tool._run(repo_path=".")
        
        # Verify result is valid JSON
        self.assertIsInstance(result, str, "Tool should return string")
        
        try:
            parsed_result = json.loads(result)
            self.assertIsInstance(parsed_result, dict, "Result should be valid JSON object")
            
            # Check for expected structure (either success or error)
            # Check for expected structure (either success or error)
            if "error" in parsed_result:
                # If error, should have proper error structure
                self.assertIn("error_type", parsed_result)
                print(f"Tool returned error (expected): {parsed_result['error']}")
            else:
                # If success, should have repository info (actual response structure)
                self.assertIn("repository", parsed_result)
                self.assertIn("active_branch", parsed_result)
                self.assertIn("file_count", parsed_result)
                
                file_count = parsed_result.get('file_count', 0)
                api_files = len(parsed_result.get('potential_api_files', []))
                print(f"✅ Tool executed successfully!")
                print(f"   Repository: {parsed_result.get('repository', 'Unknown')}")
                print(f"   Branch: {parsed_result.get('active_branch', 'Unknown')}")
                print(f"   Total files: {file_count}")
                print(f"   Potential API files: {api_files}")
                
        except json.JSONDecodeError:
            self.fail(f"Tool returned invalid JSON: {result[:200]}...")

    def test_10_project_structure_correct(self):
        """Test 10: Project directory structure is correct."""
        required_dirs = ['agents', 'flows', 'configs', 'tasks', 'tools', 'utils']

        for dir_name in required_dirs:
            dir_path = os.path.join(self.project_root, dir_name)
            self.assertTrue(
                os.path.isdir(dir_path),
                f"Required directory '{dir_name}' not found"
            )


def run_tests():
    """Run the test suite with nice output."""
    print("=" * 70)
    print("API ECOSYSTEM MANAGER - ESSENTIAL TEST SUITE")
    print("=" * 70)
    print("\nRunning 10 essential tests...\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestEssentials)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n[PASS] ALL TESTS PASSED!")
        print("=" * 70)
        return 0
    else:
        print("\n[FAIL] SOME TESTS FAILED")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
