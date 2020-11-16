#!/usr/bin/env bash

source airflow_0.sh

rm -rf \
  "${AIRFLOW_HOME}/airflow.cfg" \
  "${AIRFLOW_HOME}/airflow.db" \
  "${AIRFLOW_HOME}/unittests.cfg" \
  "${AIRFLOW_HOME}/logs/"

unset AIRFLOW_HOME
