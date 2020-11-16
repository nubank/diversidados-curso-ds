#!/usr/bin/env bash

# Airflow UI

# Constants
source airflow_0.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$env_name"

# Start the web server, default port is 8080
echo "Start the scheduler in another terminal."
echo "Starting the web server..."
echo "To open the airflow UI, visit http://localhost:8080 in the browser."
airflow webserver -p 8080
