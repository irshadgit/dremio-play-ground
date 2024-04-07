from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Define the DAG
dag = DAG(
    'echo_task',
    description='A simple Airflow DAG with a single task that echoes a message',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
)

# Define the task
echo_task = BashOperator(
    task_id='echo_message',
    bash_command='echo "Hello, Airflow!"',
    dag=dag,
)