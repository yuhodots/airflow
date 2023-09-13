from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'yuho.jeong',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def greet(name, age):
    print(f"Hello world! My name is {name} and {age} years old")


with DAG(
    dag_id='greet_python',
    default_args=default_args,
    description='This is a dag for greeting',
    start_date=datetime(2023, 9, 1, 2),
    schedule_interval='@daily'
) as dag:
    
    task1 = PythonOperator(
        task_id='first_task',
        python_callable=greet,
        op_kwargs={'name': 'Yuho Jeong', 'age': 27}
    )

    task2 = PythonOperator(
        task_id='second_task',
        python_callable=greet,
        op_kwargs={'name': 'Minsu Jeong', 'age': 24}
    )

    task3 = PythonOperator(
        task_id='third_task',
        python_callable=greet,
        op_kwargs={'name': 'Chulsu Jeong', 'age': 30}
    )

    [task1, task2] >> task3
