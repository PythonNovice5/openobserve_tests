#!/bin/bash

set -e
export PYTHONPATH=$(pwd)

echo "=== [1/3] Setting up virtual environment ==="
if [ ! -d "venv" ]; then
  echo "Creating new virtual environment..."
  python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
playwright install


# Default is head (headless=false)
HEADLESS=false

# If argument is passed, override default
if [ "$1" == "--headless" ]; then
  HEADLESS=true
fi

# Export to use in Python
export HEADLESS=$HEADLESS

echo "=== [2/3] Running UI tests ==="
# Pass headless mode as a pytest option
pytest ui_tests/tests/test_dashboard.py -v -s \
  --html=ui_tests_report.html \
  --headless=$HEADLESS


