import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'rob',
    'start_date': datetime.datetime(2021, 1, 1),
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=1),
}

with DAG (
    dag_id = 'jobs_scraper_dag',
    default_args=default_args,
    schedule_interval=None, # '0 15 * * *',
    catchup=False,
) as dag:
    
    scrape_results = BashOperator(
        task_id='scrape_results',
        bash_command='''
            cd ~/code/jobs-scraper
            source ~/venv/bin/activate
            python3 main.py scrape_results
        ''',
    )

    load_results = BashOperator(
        task_id='load_results',
        bash_command='''
            cd ~/code/jobs-scraper
            source ~/venv/bin/activate
            python3 main.py load_results
        ''',
    )

    scrape_posts = BashOperator(
        task_id='scrape_posts',
        bash_command='''
            cd ~/code/jobs-scraper
            source ~/venv/bin/activate
            python3 main.py scrape_posts
        ''',
    )

    load_posts = BashOperator(
        task_id='load_posts',
        bash_command='''
            cd ~/code/jobs-scraper
            source ~/venv/bin/activate
            python3 main.py load_posts
        ''',
    )

    scrape_results >> load_results >> scrape_posts >> load_posts