import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Adding the folder to path
import os, sys
sys.path.append(os.path.dirname(__file__))
from src.result.scrape_results import run_results
from src.post.scrape_posts import run_posts


default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2021, 1, 1),
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=1),
    'catchup': False,
}

with DAG (
    dag_id = 'jobs_scraper_dag',
    default_args=default_args,
    schedule_interval = None, # '0 15 * * *',
    catchup = False,
) as dag:

    results_scrape = PythonOperator(
        task_id='results_scrape',
        python_callable=run_results,
    )

    post_scrape = PythonOperator(
        task_id='posts_scrape',
        python_callable=run_posts,
    )

    results_scrape >> post_scrape 
