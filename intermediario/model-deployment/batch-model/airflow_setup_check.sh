#!/usr/bin/env bash

# Airflow setup

# Constants
source airflow_0.sh

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate "$env_name"

# Check if nothing is wrong (there should be no error message)
python "${AIRFLOW_HOME}/dags/dag.py"

# List the DAGs
airflow list_dags
echo "To remove the examples, set 'load_examples = False' in 'airflow.cfg'."
