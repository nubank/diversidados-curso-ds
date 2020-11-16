#!/usr/bin/env bash

# Airflow setup

# Constants
source airflow_0.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$env_name"

# Initialize the database
pushd "${AIRFLOW_HOME}" 1>/dev/null
airflow initdb
popd 1>/dev/null
