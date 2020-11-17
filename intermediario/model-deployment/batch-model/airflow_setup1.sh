#!/usr/bin/env bash

# Airflow setup

# Constants
source airflow_0.sh

# Create conda environment
conda create -yn "$env_name" python=3.6 virtualenv scikit-learn pandas
eval "$(conda shell.bash hook)"
conda activate "$env_name"

echo "Current conda environment = $(conda env list | grep '*')"

# Install
python -m pip install 'apache-airflow'
