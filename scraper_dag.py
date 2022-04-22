### To solve "Hostname of job runner does not match", set "hostname_callable = socket.gethostname" in airflow.cfg.
# One dot, no column, otherwise it gets corrected... and the scheduler gets stuck until it restarts 
# (because of SequentialExecutor and sqlite, during the execution, the scheduler has no heartbeat and doesn't progress)
### If the scheduler gets stuck and the task stays is queued, check for errors or corrections in console
# https://stackoverflow.com/questions/57681573/how-to-fix-the-error-airflowexceptionhostname-of-job-runner-does-not-match

from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Adding the folder to path
# ~ has to be expanded. works both on macos and linux
import os
import sys
path = os.path.expanduser('~/airflow/dags/jobs-scraper/')
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
