#!/bin/bash

set -e

echo "=== [1/5] Starting infrastructure setup ==="

ZIP_FILE="k8slog_json.json.zip"
JSON_FILE="k8slog_json.json"
DOCKER_NAME="openobserve-test"

# Step 1: Download data only if not already present
if [ ! -f "$ZIP_FILE" ]; then
  echo "Downloading data file..."
  curl -L https://zinc-public-data.s3.us-west-2.amazonaws.com/zinc-enl/sample-k8s-logs/$ZIP_FILE -o $ZIP_FILE
else
  echo "Data zip file already exists: $ZIP_FILE — skipping download."
fi

# Step 2: Unzip only if .json file not present
if [ ! -f "$JSON_FILE" ]; then
  echo "Unzipping data file..."
  unzip -o $ZIP_FILE
else
  echo "Unzipped JSON file already exists: $JSON_FILE — skipping unzip."
fi

# Step 3: Start container only if not already running
if [ "$(docker ps -q -f name=$DOCKER_NAME)" ]; then
  echo "Docker container '$DOCKER_NAME' is already running — skipping start."
else
  if [ "$(docker ps -aq -f name=$DOCKER_NAME)" ]; then
    echo "Container exists but not running — starting it..."
    docker start $DOCKER_NAME
  else
    echo "Starting new OpenObserve Docker container '$DOCKER_NAME'..."
    docker run -d \
      -v $PWD/data:/data \
      -e ZO_DATA_DIR="/data" \
      -e ZO_ROOT_USER_EMAIL="root@example.com" \
      -e ZO_ROOT_USER_PASSWORD="Complexpass#123" \
      -p 5080:5080 \
      --name $DOCKER_NAME \
      public.ecr.aws/zinclabs/openobserve:latest
  fi

  echo "Waiting 10 seconds for OpenObserve to start..."
  sleep 10
fi

# Step 4: Ask if user wants to upload data again
read -p "Do you want to (re)upload data to OpenObserve? (y/n): " choice
if [[ "$choice" =~ ^[Yy]$ ]]; then
  echo "Uploading logs to OpenObserve..."
  curl -s -o /dev/null -w "%{http_code}\n" \
    -u "root@example.com:Complexpass#123" \
    -H "Content-Type: application/json" \
    --data-binary "@$JSON_FILE" \
    http://localhost:5080/api/default/default/_json
    # Save timestamp after upload
    upload_time=$(date +%s%6N)
    echo "Upload timestamp captured: $upload_time"
    echo $upload_time > upload_time.txt
else
  echo "Skipping data upload."
fi

echo "=== [5/5] Infrastructure setup complete ==="
