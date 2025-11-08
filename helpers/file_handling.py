import json
import logging
import os

logger = logging.getLogger(__name__)

def load_test_data(file_name):
    """Helper function to load test data from a JSON file in the testdata directory."""
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    logger.info(f"Loading json testdata from {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
