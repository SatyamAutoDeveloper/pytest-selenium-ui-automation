# pytest-selenium-ui-automation
UI Automation using Selenium, Python and Pytest Framework.

## Environment Setup
Download and Install Python 3.10+ version

## Project Structure

```
pytest-selenium-ui-automation/
├── pages/                 # Page Object Model classes
├── tests/                 # Test scripts organized by feature
├── testdata/              # Test data files(.json)
├── config.ini             # Configuration files and settings
├── helpers/               # Helper functions, file handling and driver utilities
├── locators/              # UI element locators
├── reports/               # Test execution reports will be generated on runtime
├── screenshots/           # Screenshots captured during tests on failure on runtime
├── logs/                  # Test execution logs will be generated on runtime
├── conftest.py            # Pytest fixtures and setup/teardown methods
├── requirements.txt       # Python dependencies
└── pytest.ini             # For custom markers, logging and html report configuration.
```

## Setup and Installation

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Update configuration files as needed

## Command for Running Tests

```bash
pytest tests/ # To run all tests in the tests directory
pytest --headless tests/ # To run all tests in headless mode
pytest tests/test_yatra_hotel_feature.py -m "positive" # To run tests with a specific marker
```

## Reporting
After test execution, HTML reports will be generated in the `reports/` directory. Logs will be available in the `logs/` directory and screenshots of failed tests will be saved in the `screenshots/` directory.


## Custom Markers
- `@pytest.mark.positive`: Marks positive test cases.
- `@pytest.mark.negative`: Marks negative test cases.
- `@pytest.mark.edge`: Marks edge test cases.


## retry logic on failed actions for selenium actions
Implemented retry logic for selenium actions to handle transient issues during UI interactions. This ensures that temporary glitches do not cause test failures, improving the reliability of the test suite.


## Uploading Artifacts after each execution with zipping(HTML Report, Screenshots, Logs) in the Pipeline.
- Run the yatra_ui.yml Workflow in github actions to generate HTML Report along with logs and screenshots from the Pipeline.
- Run the yatra_ui_parallel_execution.yml Workflow in github actions to generate Allure Report along with logs and screenshots from the Pipeline with Parallel Execution.
- Run the heroku_ui_self_healing_using_ollama.yml Workflow in github actions to generate HTML Report along with logs and screenshots from the Pipeline with Self-Healing Agent using Ollama Model.
- All artifacts will be uploaded after each execution in the workflow run.


# To Generate Allure Report in Local Machine
## Note:
- Ensure Java is installed on your machine to run Allure reports.
## Setup Command Line Tool for Azure:
  - Download Zip: https://github.com/allure-framework/allure2/releases/tag/2.35.1
  - Add allure/bin to system variable path.
## Run the below Command to Setup Allure on Project Level:
  - pip install allure-pytest
  - npm install -g allure-commandline
## Configure below line in pytest.ini file for Allure Raw Results:
  - addopts = --alluredir=allure-results
- To Generate and Open Allure HTML Report: run command: allure serve allure-results


## Performance Optimization:
I have integrated parallelism into the test suite to optimize CI/CD throughput. Using the pytest-xdist plugin, the execution is distributed across multiple workers within the GitHub Actions runner.
- Framework: Pytest with Selenium WebDriver.
- Execution Strategy: Multi-process concurrent execution (pytest -n auto).
- Impact: Achieved a 3x reduction in total execution time compared to sequential runs, significantly lowering the overhead of the automated regression suite.


## Self-Healing Agent Documentation
Detailed Documentation Link for Self-Healing Agent: [https://github.com/SatyamAutoDeveloper/pytest-selenium-ui-automation/wiki/Self%E2%80%90Healing-Agent-Documentation]