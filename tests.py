import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class TestEnterpriseAPIEcosystem(unittest.TestCase):
    """Comprehensive test suite for Enterprise API Ecosystem Manager."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
    def test_01_environment_setup(self):
        """Test that environment is properly configured."""
        env_example_path = os.path.join(self.project_root, '.env.example')
        self.assertTrue(os.path.exists(env_example_path), ".env.example file not found")
        
    def test_02_config_file_exists(self):
        """Test that configuration file exists and is valid."""
        config_path = os.path.join(self.project_root, 'configs', 'app_config.json')
        self.assertTrue(os.path.exists(config_path), "app_config.json not found")
        
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.assertIn('llm_config', config)
        self.assertIn('model', config['llm_config'])
        
    def test_03_agent_creation(self):
        """Test that all agents can be created successfully."""
        from agents.api_discovery_agent import create_api_discovery_agent
        from agents.documentation_agent import create_documentation_agent
        from agents.compliance_agent import create_compliance_agent
        from agents.developer_experience_agent import create_developer_experience_agent
        
        # Note: These will fail without GEMINI_API_KEY, but structure is correct
        try:
            discovery_agent = create_api_discovery_agent()
            self.assertIsNotNone(discovery_agent)
        except ValueError as e:
            self.assertIn("GEMINI_API_KEY", str(e))
            
    def test_04_task_definitions(self):
        """Test that task definitions are properly structured."""
        from tasks.discovery_tasks import discovery_task
        from tasks.documentation_tasks import documentation_task
        from tasks.compliance_tasks import compliance_task
        from tasks.developer_experience_tasks import developer_experience_task
        
        self.assertIsNotNone(discovery_task)
        self.assertIsNotNone(documentation_task)
        self.assertIsNotNone(compliance_task)
        self.assertIsNotNone(developer_experience_task)
        
    def test_05_network_scanner_tool(self):
        """Test network scanner tool instantiation."""
        from tools.network_scanner import NetworkScannerTool
        
        tool = NetworkScannerTool()
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Network Scanner Tool")
        
    def test_06_git_analyzer_tool(self):
        """Test git repository analyzer tool instantiation."""
        from tools.git_analyzer import GitRepositoryAnalyzerTool
        
        tool = GitRepositoryAnalyzerTool()
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Git Repository Analyzer Tool")
        
    def test_07_security_scanner_tool(self):
        """Test security scanner tool instantiation."""
        from tools.security_scanner import SecurityScannerTool
        
        tool = SecurityScannerTool()
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Security Scanner Tool")
        
    def test_08_documentation_builder_tool(self):
        """Test documentation builder tool instantiation."""
        from tools.documentation_builder import DocumentationBuilderTool
        
        tool = DocumentationBuilderTool()
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "Documentation Builder Tool")
        
    def test_09_sdk_generator_tool(self):
        """Test SDK generator tool instantiation."""
        from tools.sdk_generator import SDKGeneratorTool
        
        tool = SDKGeneratorTool()
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "SDK Generator Tool")
        
    def test_10_output_handler_utilities(self):
        """Test output handler utility functions exist and are importable."""
        from utils.output_handler import (
            save_complete_output,
            extract_and_save_components,
            process_and_save_results
        )
        
        self.assertTrue(callable(save_complete_output))
        self.assertTrue(callable(extract_and_save_components))
        self.assertTrue(callable(process_and_save_results))
        
    def test_11_llm_config_utilities(self):
        """Test LLM configuration utilities."""
        from utils.llm_config import load_config, get_llm_config
        
        self.assertTrue(callable(load_config))
        self.assertTrue(callable(get_llm_config))
        
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn('llm_config', config)
        
    def test_12_crew_orchestration(self):
        """Test crew orchestration class."""
        from crew import APIEcosystemCrew
        
        # Test class can be instantiated (will fail without API key)
        try:
            crew = APIEcosystemCrew(verbose=False)
            self.assertIsNotNone(crew)
        except ValueError as e:
            self.assertIn("GEMINI_API_KEY", str(e))
            
    def test_13_main_entry_point(self):
        """Test that main.py has correct structure."""
        main_path = os.path.join(self.project_root, 'main.py')
        self.assertTrue(os.path.exists(main_path), "main.py not found")
        
        with open(main_path, 'r') as f:
            content = f.read()
        
        # Verify main.py imports from utils.output_handler
        self.assertIn('from utils.output_handler import', content)
        self.assertIn('process_and_save_results', content)
        
        # Verify main.py has main() function
        self.assertIn('def main():', content)
        
    def test_14_no_async_crew_file(self):
        """Test that async_crew.py has been removed (FIXED)."""
        async_crew_path = os.path.join(self.project_root, 'async_crew.py')
        self.assertFalse(os.path.exists(async_crew_path), 
                        "async_crew.py should be removed (dead code)")
        
    def test_15_main_file_simplified(self):
        """Test that main.py is simplified (FIXED)."""
        main_path = os.path.join(self.project_root, 'main.py')
        
        with open(main_path, 'r') as f:
            lines = f.readlines()
        
        # Main file should be significantly smaller (around 64 lines)
        self.assertLess(len(lines), 100, 
                       "main.py should be simplified (< 100 lines)")
        
        # Should not contain utility function definitions
        content = ''.join(lines)
        self.assertNotIn('def save_complete_output', content,
                        "Utility functions should be in utils/output_handler.py")
        self.assertNotIn('def extract_and_save_components', content,
                        "Utility functions should be in utils/output_handler.py")
        
    def test_16_utils_output_handler_exists(self):
        """Test that utils/output_handler.py exists (FIXED)."""
        output_handler_path = os.path.join(self.project_root, 'utils', 'output_handler.py')
        self.assertTrue(os.path.exists(output_handler_path),
                       "utils/output_handler.py should exist")
        
        with open(output_handler_path, 'r') as f:
            content = f.read()
        
        # Verify it contains the moved functions
        self.assertIn('def save_complete_output', content)
        self.assertIn('def extract_and_save_components', content)
        self.assertIn('def process_and_save_results', content)
        
    def test_17_project_structure(self):
        """Test that project structure is correct."""
        required_dirs = ['agents', 'configs', 'tasks', 'tools', 'utils']
        
        for dir_name in required_dirs:
            dir_path = os.path.join(self.project_root, dir_name)
            self.assertTrue(os.path.isdir(dir_path), 
                          f"Required directory '{dir_name}' not found")
            
    def test_18_requirements_file(self):
        """Test that requirements.txt exists and has required packages."""
        req_path = os.path.join(self.project_root, 'requirements.txt')
        self.assertTrue(os.path.exists(req_path), "requirements.txt not found")
        
        with open(req_path, 'r') as f:
            requirements = f.read()
        
        required_packages = ['crewai', 'python-dotenv', 'GitPython', 'requests']
        for package in required_packages:
            self.assertIn(package, requirements, 
                         f"Required package '{package}' not in requirements.txt")
            
    def test_19_dockerfile_exists(self):
        """Test that Dockerfile exists."""
        dockerfile_path = os.path.join(self.project_root, 'Dockerfile')
        self.assertTrue(os.path.exists(dockerfile_path), "Dockerfile not found")
        
    def test_20_documentation_exists(self):
        """Test that documentation files exist."""
        doc_files = ['README.md', 'CHANGELOG.md', 'FIXES.md']
        
        for doc_file in doc_files:
            doc_path = os.path.join(self.project_root, doc_file)
            self.assertTrue(os.path.exists(doc_path), 
                          f"Documentation file '{doc_file}' not found")


class TestCodeQualityFixes(unittest.TestCase):
    """Test suite specifically for code review fixes."""
    
    def test_fix_1_async_crew_removed(self):
        """Verify Fix 1: async_crew.py has been removed."""
        project_root = os.path.dirname(os.path.abspath(__file__))
        async_crew_path = os.path.join(project_root, 'async_crew.py')
        
        self.assertFalse(os.path.exists(async_crew_path),
                        "FIX 1 FAILED: async_crew.py should be removed")
        
    def test_fix_2_main_simplified(self):
        """Verify Fix 2: main.py has been simplified."""
        project_root = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(project_root, 'main.py')
        
        with open(main_path, 'r') as f:
            content = f.read()
            lines = len(content.split('\n'))
        
        # Main should be less than 100 lines
        self.assertLess(lines, 100,
                       "FIX 2 FAILED: main.py should be simplified")
        
        # Should import from utils.output_handler
        self.assertIn('from utils.output_handler import', content,
                     "FIX 2 FAILED: Should import from utils.output_handler")
        
    def test_fix_2_output_handler_created(self):
        """Verify Fix 2: utils/output_handler.py has been created."""
        project_root = os.path.dirname(os.path.abspath(__file__))
        output_handler_path = os.path.join(project_root, 'utils', 'output_handler.py')
        
        self.assertTrue(os.path.exists(output_handler_path),
                       "FIX 2 FAILED: utils/output_handler.py should exist")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
