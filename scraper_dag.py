### To solve "Hostname of job runner does not match", set "hostname_callable = socket.gethostname" in airflow.cfg.
# One dot, no column, otherwise it gets corrected... and the scheduler gets stuck until it restarts 
# (because of SequentialExecutor and sqlite, during the execution, the scheduler has no heartbeat and doesn't progress)
### If the scheduler gets stuck and the task stays is queued, check for errors or corrections in console
# https://stackoverflow.com/questions/57681573/how-to-fix-the-error-airflowexceptionhostname-of-job-runner-does-not-match

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

## AIRFLOW__SCHEDULER__SCHEDULE_AFTER_TASK_EXECUTION = False

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
