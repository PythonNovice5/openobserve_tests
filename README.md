# OpenObserve Testing Framework
This repository provides an automated testing framework for Frontent end and backend tests for OpenObserve. It includes test cases to validate OpenObserve's search APIs and dashboard creation using sample Kubernetes log data. The setup scripts also handle the test infrastructure by spinning up OpenObserve in a Docker container.

##  Features

- Downloads and extracts sample Kubernetes logs
- Spins up an OpenObserve Docker container
- (Re)uploads log data to OpenObserve
- Captures upload timestamp
- Sets up a Python virtual environment
- Installs dependencies
- Runs API tests using `pytest`+`requests`
- Runs UI tests using `pytest` + `Playwright`
- Provides optional Docker container cleanup

##  Files

- `k8slog_json.json.zip`: Compressed sample Kubernetes logs (downloaded automatically)
- `k8slog_json.json`: Unzipped JSON logs
- `upload_time.txt`: Timestamp of the last data upload

##  How to Use

### Setup OpenObserve server

```bash
./infra_setup.sh
```

This will:

- Download and unzip log files
- Start the Docker container (if not already running)
- Prompt to (re)upload logs to OpenObserve
- Save the upload timestamp to upload_time.txt


### API Testing

```bash
./run_api_tests.sh
```

The script performs:

- Creates a new Python virtual environment if not already present
- Activates the environment
- Installs dependencies from requirements.txt
- Executes tests located in `api_tests/test_search_api.py`
- Generates an HTML report (`api_test_report.html`)

### UI Testing

```bash
./run_ui_tests.sh
```

The script performs:

- Creates and activates the Python virtual environment
- Installs project dependencies from `requirements.txt`
- Installs Playwright
- Executes UI tests located in ui_tests/tests/test_dashboard.py
- Generates a standalone HTML report: `ui_tests_report.html`

To run tests in headless mode (no browser window):
```bash
./run_ui_tests.sh --headless
```

```bash
./cleanup.sh
```

- Cleans up the docker container

### Logging & Reports

The framework generates logs and reports for debugging:

- **HTML Reports:**
  - API: `api_test_report.html`
  - UI: `ui_tests_report.html`

- **Log Files:**
  - **API Logs:** `api_tests/api_test.log`
  - **UI Logs:** `ui_tests/ui_test.log`
  - Includes timestamps and test execution details (setup, upload events, errors)


###  Future Improvements & TODOs

While the current testing framework provides end-to-end coverage for both API and UI layers, there are several enhancements and best practices we aimed to implement but couldn't due to time constraints:

- **Incomplete UI testing**  
  Currently, UI test is not completed e2e as the requirements for the verifications were not clear, this can be accomplished by discussing and going through the application in a scheduled meeting

- **Cross-Browser UI Testing**  
  Currently, UI tests are limited to a single browser (e.g., Chromium). Adding support for Firefox and WebKit via Playwright would improve cross-browser reliability.

- **CI/CD Integration**  
  Automating tests through GitHub Actions or GitLab CI/CD would enable continuous integration with every code push or pull request.

- **Test Coverage Reporting**  
  Integrating tools like `pytest-cov` for API and `allure` or `reportportal` for UI tests would help measure and visualize test coverage.

- **Parameterized Testing**  
  Test cases (especially API and UI login tests) can be enhanced with parameterization for multiple user roles, edge cases, and invalid inputs.

- **Data Isolation**  
  Current tests may use some data which could be isolated from the tests in the form of json, csv or yeml files for better reusability and modularity

- **Environment Config Management**  
  Switching to a more dynamic configuration approach if we have multiple environments to validate our product under test

- **Credential Encryption or Secrets Management**  
  For security, storing credentials in encrypted form or integrating with secrets managers (e.g., HashiCorp Vault, AWS Secrets Manager) would be ideal.

- **Test Tagging and Selective Execution**  
  Use `pytest` markers (like `@pytest.mark.smoke`, `@pytest.mark.regression`) to allow selective test runs, in case we have multiple tests

- **UI Page Object Enhancements**  
  The current Page Object Model (POM) can be further modularized to support component-level abstraction for better reusability.
