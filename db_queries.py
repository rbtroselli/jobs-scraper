# class, to keep db connection?
import duckdb

def copy_search_results():
    conn = duckdb.connect('./data/jobs.db')
    conn.execute("""
        COPY raw_search_result (id, url, search_terms, scrape_timestamp)
        FROM './data/results.csv' (delimiter '|', header true)
        ;
    """)
    return

def insert_new_search_results():
    conn = duckdb.connect('./data/jobs.db')
    conn.execute("""
        INSERT INTO search_result (id, url, search_terms, scrape_timestamp)
        SELECT id, url, search_terms, scrape_timestamp
        FROM raw_search_result
        WHERE 
            insert_update_timestamp > (SELECT last_run_timestamp FROM flow_run_cfg WHERE source='raw_search_result')
            AND id NOT IN (SELECT id FROM search_result)
        ;
    """)
    return

def update_search_result_last_run():
    conn = duckdb.connect('./data/jobs.db')
    conn.execute("""
        UPDATE flow_run_cfg
        SET last_run_timestamp = CURRENT_TIMESTAMP
        WHERE source='raw_search_result'
        ;
    """)
    return

# if __name__ == '__main__':
#     copy_search_results()
#     insert_new_search_results()
#     update_search_result_last_run()
