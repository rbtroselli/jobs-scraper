import sqlite3
import pandas as pd

def jobs_loader(path=''):
    staging_file = path + 'data/staging.csv'
    db = path + 'data/jobs.db'

    # read staging csv, then load everything in the db (automatically creating and replacing table)
    connection = sqlite3.connect(db)
    df = pd.read_csv(staging_file)
    # drop duplicates based on job_id (that is used as PK). There may be "data engineer/data scientist" posts
    df = df.drop_duplicates(subset='job_id', keep='first')
    df.to_sql('new_jobs', connection, if_exists='replace', index=False, dtype={'job_id': 'TEXT PRIMARY KEY'})
    connection.close()
    return


def jobs_merger(path=''):
    db = path + 'data/jobs.db'
    
    # sqlite has no MERGE
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO jobs
        SELECT *
        FROM new_jobs
        WHERE job_id NOT IN (SELECT job_id FROM jobs) """)
    connection.commit()
    connection.close() 
    return


if __name__ == "__main__":
    jobs_loader()
    jobs_merger()

