# OpenObserve Infrastructure Setup Script

This repository includes a simple shell script to automate the setup of an OpenObserve environment, including downloading sample Kubernetes logs, spinning up a Docker container, and uploading the logs into OpenObserve.

##  Features

- Downloads and extracts sample Kubernetes logs
- Spins up an OpenObserve Docker container
- Sets up a Python virtual environment
- Installs dependencies
- Runs API tests using `pytest`
- (Optionally) uploads log data to OpenObserve
- Captures upload timestamp
- Provides optional Docker container cleanup

##  Files

- `k8slog_json.json.zip`: Compressed sample Kubernetes logs (downloaded automatically)
- `k8slog_json.json`: Unzipped JSON logs
- `upload_time.txt`: Timestamp of the last data upload

## 🐚 How to Use

### Setup OpenObserve server

```bash
./infra_setup.sh
```

This will:

- Download and unzip log files (if needed)
- Start the Docker container (if not already running)
- Prompt to (re)upload logs to OpenObserve
- Save the upload timestamp to upload_time.txt

### API Testing

```bash
./run_tests.sh
```

The script performs:

- Creates a new Python virtual environment if not already present
- Activates the environment
- Installs dependencies from requirements.txt
- API Testing
- Executes tests located in api_tests/test_search_api.py
- Generates an HTML report (report.html)
