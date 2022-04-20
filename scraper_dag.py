from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Adding the folder to path
path = '/Users/robertoroselli/airflow/dags/jobs-scraper/'
import sys
sys.path.append(path)
from jobs_scraper import url_scraper
from jobs_scraper import post_scraper
from jobs_loader import jobs_loader
from jobs_loader import jobs_merger


# default_args
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

# instantiate DAG
with DAG(
    'scraper_dag',
    default_args=default_args,
    description='A for scheduling my job posts scraping tool',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:

    # tasks
    url_scrape = PythonOperator(
        task_id='url_scrape',
        python_callable=url_scraper,
        op_args=[path],
    )

    post_scrape = PythonOperator(
        task_id='post_scrape',
        python_callable=post_scraper,
        op_args=[path],
    )

    jobs_load = PythonOperator(
        task_id='jobs_load',
        python_callable=jobs_loader,
        op_args=[path],
    )

    jobs_merge = PythonOperator(
        task_id='jobs_merge',
        python_callable=jobs_merger,
        op_args=[path],
    )

    # pipeline
    url_scrape >> post_scrape >> jobs_load >> jobs_merge
