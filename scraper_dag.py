# [START import_module]
from datetime import timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

path = '/Users/robertoroselli/airflow/dags/jobs-scraper/'

import sys
sys.path.append(path)


from jobs_scraper import url_scraper
from jobs_scraper import post_scraper

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'email': ['airflow@example.com'],
    #'email_on_failure': False,
    #'email_on_retry': False,
    #'retries': 1,
    #'retry_delay': timedelta(minutes=5),
    ##'catchup_by_default' : False
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'scraper_dag',
    default_args=default_args,
    description='A for scheduling my job posts scraping tool',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
    catchup=False,
    ##schedule_interval=None,
) as dag:
    # [END instantiate_dag]

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    # [START basic_task]
    t1 = PythonOperator(
        task_id='url_scrape',
        python_callable=url_scraper,
        op_args=[path],
    )

    t2 = PythonOperator(
        task_id='post_scrape',
        python_callable=post_scraper,
        op_args=[path],
        # retries=3,
    )
    # [END basic_task]

    t1 >> t2
