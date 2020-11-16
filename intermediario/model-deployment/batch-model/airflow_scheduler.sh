#!/usr/bin/env bash

# Airflow scheduler

# Constants
source airflow_0.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$env_name"

# Start the scheduler
echo "Starting the scheduler..."
airflow scheduler
