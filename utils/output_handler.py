import os
import re
import logging

logger = logging.getLogger(__name__)


def save_complete_output(result):
    """
    Save the complete output to a text file.
    
    Args:
        result: The result from crew execution
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs("outputs", exist_ok=True)
        
        with open("outputs/complete_output.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
            
        logger.info("Complete output saved to outputs/complete_output.txt")
        return True
        
    except Exception as e:
        logger.error(f"Error saving complete output: {e}")
        return False


def extract_and_save_components(content):
    """
    Extract components from the complete output and save them separately.
    
    Args:
        content: The complete output content as string
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs("outputs/docs", exist_ok=True)
        os.makedirs("outputs/sdks/python", exist_ok=True)
        os.makedirs("outputs/sdks/javascript", exist_ok=True)
        
        logger.info("Extracting and saving components...")
        
        # Extract Python SDK
        python_sdk_pattern = r"```python\s*\n(.*?class\s+.*?Client.*?)\s*```"
        python_sdk_match = re.search(python_sdk_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if python_sdk_match:
            python_sdk = python_sdk_match.group(1)
            with open("outputs/sdks/python/enterprise_api_client.py", "w", encoding="utf-8") as f:
                f.write(python_sdk)
            logger.info("Python SDK saved to outputs/sdks/python/enterprise_api_client.py")
        else:
            logger.info("No Python SDK found in output")
        
        # Extract JavaScript SDK
        js_sdk_pattern = r"```javascript\s*\n(.*?class\s+.*?Client.*?)\s*```"
        js_sdk_match = re.search(js_sdk_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if js_sdk_match:
            js_sdk = js_sdk_match.group(1)
            with open("outputs/sdks/javascript/enterprise_api_client.js", "w", encoding="utf-8") as f:
                f.write(js_sdk)
            logger.info("JavaScript SDK saved to outputs/sdks/javascript/enterprise_api_client.js")
        else:
            logger.info("No JavaScript SDK found in output")
        
        # Save documentation
        with open("outputs/docs/api_documentation.md", "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("Documentation saved to outputs/docs/api_documentation.md")
        
        logger.info("Component extraction and saving completed!")
        return True
        
    except Exception as e:
        logger.error(f"Error extracting and saving components: {e}")
        return False


def process_and_save_results(result):
    """
    Process crew execution results and save all outputs.
    
    This is a convenience function that combines saving and extraction.
    
    Args:
        result: The result from crew execution
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not save_complete_output(result):
            logger.error("Failed to save complete output")
            return False
        
        with open("outputs/complete_output.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        return extract_and_save_components(content)
        
    except Exception as e:
        logger.error(f"Error processing and saving results: {e}")
        return False
