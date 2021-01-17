[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PyPI version](https://badge.fury.io/py/publish-event-sns.svg)](https://badge.fury.io/py/airflow-notity-sns)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/msantino.svg?style=social&label=Follow)](https://twitter.com/msantino)


# Publish Airflow Notification to a SNS Topic

This package adds a callback function to use in failures to DAGs and Tasks in a Airflow project. 


## Installation

```bash
pip install airflow-notify-sns
```


## Usage

```python
from datetime import timedelta

# Airflow native imports to create a DAG
from airflow import DAG, utils
from airflow.operators.bash_operator import BashOperator

# Here is function import
from airflow_notify_sns import airflow_notify_sns

# Dag Definition
dag = DAG(
    dag_id='test_dag',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': utils.dates.days_ago(1),
        'retries': 3,
        'retry_delay': timedelta(minutes=5)
    },
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    sla_miss_callback=airflow_notify_sns
)

# Add your tasks here
t = BashOperator(
    dag=dag,
    task_id='test_env',
    bash_command='/tmp/test.sh',
    env={'EXECUTION_DATE': '{{ ds }}'},
    on_failure_callback=airflow_notify_sns
)
```

When DAG or tasks ends in error, a notification will be send to a SNS Topic using AWS default connection (`aws_default`). 

## Required Variable

This module will try to find a variable named `airflow_notify_sns_arn` in your Airflow environment, containing SNS Topic ARN where message will be published to. 

If variable is not found, function will abort execution with no error. 