import csv
import logging
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from extract_imdb import extract

default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'dag_ELT_website_postgres_minios3',
    default_args=default_args,
    start_date=datetime(2024, 10, 8),
    schedule_interval='@daily'
)as dag:
    task1 = PythonOperator(
        task_id= "imdb_to_minio",
        python_callable=extract
    )
    task1