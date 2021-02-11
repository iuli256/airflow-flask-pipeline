from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from spanish_address_plugin.operators.address_source_list import AddressSourceListOperator
from spanish_address_plugin.operators.process_address import ProcessAddressOperator

default_args = {
    'owner': 'iulian-craciun',
    'start_date': datetime(2021, 1, 1),
    'depends_on_past': False,
    'email': ['ahmadchaiban@gmail.com'],
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

dag = DAG(
    'Spanish_address_pipeline',
    default_args=default_args,
    description='Load and transform data in Mongo with Airflow',
    schedule_interval=None
)

start_operator = DummyOperator(
    task_id='Begin_execution',
    dag=dag
)

address_source_list = AddressSourceListOperator(
    task_id='get_source_list',
    dag=dag,
    table='data_feed',
    conn_id = 'local_postgresql',
    scraped_folder = '/usr/local/airflow/scraped_files/'
)

process_address = ProcessAddressOperator(
    task_id='process_source_list',
    dag=dag,
    table='data_feed',
    conn_id = 'local_postgresql',
    scraped_folder = '/usr/local/airflow/scraped_files/'
)

start_operator >> address_source_list >> process_address