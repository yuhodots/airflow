# Airflow

## Basics

- DAG: A collection of tasks
- Task: Task implements operators
- Operator: BashOperator, PythonOperator, etc.
- Task Lifecycle: `no_status` -> Scheduler -> `{status}` -> Executor -> `{status}` -> Worker -> `{status}`
  - status: no_status, scheduled, upstream_failed, queued, running, success, failed, up_for_retry, up_for_rescehdule, skipped, etc.
  

### Fundamental Features

- [Airflow Fundamentals](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html#)
- [Airflow Templates Reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#templates-reference)

1. BashOperator
2. PythonOperator
3. XComs (i.e., cross-communications)
4. Taskflow API (with @dag and @task decorator)
5. Catch-Up and Backfill
6. Scheduler with Cron Expression (https://crontab.guru)
7. Docker Install Python Package
8. PostgressOperator
9. AWS S3 Sensor Operator
10. Hooks

## Installation

In this repo, just run `docker-compose up -d` and check web server in localhost:8080/

You can create user in web server with `airflow users create`

### Airflow Locally

1. Install airflow: https://github.com/apache/airflow

```
pip install 'apache-airflow==2.7.1' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.8.txt"
```

2. `export AIRFLOW_HOME=.`
3. `airflow db init`
4. `airflow webserver -p 8080` and check web server in localhost:8080/
5. Set username and password w. `airflow users create --help`
6. `airflow scheduler`

### Airflow in Docker

1. Get docker-compose file for airflow

```
curl -Lf0 'https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml"
```

2. `mkdir ./dags ./logs ./plugins`
3. `docker-compose up airflow-init`
4. `docker-compose up -d` and check web server in localhost:8080/

## Quick Start

- Wonderful example codes are [here](https://github.com/coder2j/airflow-docker/tree/main/dags) and [here](https://www.youtube.com/watch?v=K9AnJ9_ZAXE&t=37s)
- You can check the results of tasks in the Log of the Airflow webserver (0.0.0.0:8080/)

### BashOperator

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
  'owner': 'yuhodots',
  'retries': 5,
  'retry_delay': timedelta(minutes=2)
}

with DAG(
	dag_id='first_dag',
  default_args=default_args,
  description='first dag'
  start_date=datetime(2023, 9, 1, 2),
  schedule_interval='@daily'
) as dag:
  
  task1 = BashOperator(
  	task_id='first_task',
    bash_command="echo hello world, this is the first task!"
  )

  task2 = BashOperator(
  	task_id='second_task',
    bash_command="echo hello world, this is the second task!"
  )

  task1 >> task2	# same with `task1.set_downstream(task2)`
```

### PythonOperator

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
  'owner': 'yuhodots',
  'retries': 5,
  'retry_delay': timedelta(minutes=2)
}

def greet(name, age):
  print(f"Hello world! My name is {name} and {age} years old")

with DAG(
	dag_id='first_dag',
  default_args=default_args,
  description='first dag'
  start_date=datetime(2023, 9, 1, 2),
  schedule_interval='@daily'
) as dag:
  
  task1 = PythonOperator(
  	task_id='first_task',
    python_callable=greet,
    op_kwargs={'name': 'Yuho Jeong', 'age': 27}
  )

  task1
```
