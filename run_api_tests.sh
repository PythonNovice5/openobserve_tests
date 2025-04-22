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
pip install -r requirements.txt

echo "=== [2/3] Running API tests ==="
pytest api_tests/test_search_api.py -v -s --html=api_test_report.html


