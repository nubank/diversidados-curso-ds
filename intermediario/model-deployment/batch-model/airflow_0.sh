#!/usr/bin/env bash

# Airflow constants

# Set Airflow home (optional; default: ~/airflow)
base_dir="$(pwd)"
export AIRFLOW_HOME="${base_dir}/airflow_home"

env_name="airflow-batch-model"
