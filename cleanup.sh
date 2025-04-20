#!/bin/bash

echo "=== [1/1] Cleaning up Docker container ==="

# Stop and remove the OpenObserve container if it exists
if [ "$(docker ps -q -f name=openobserve-test)" ]; then
    echo "Stopping running container: openobserve-test"
    docker stop openobserve-test
fi

if [ "$(docker ps -aq -f name=openobserve-test)" ]; then
    echo "Removing container: openobserve-test"
    docker rm openobserve-test
    echo "Cleanup complete."
else
    echo "No container named 'openobserve-test' found."
fi


