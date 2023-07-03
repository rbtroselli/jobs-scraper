import duckdb
def copy_search_results():
    conn = duckdb.connect('./data/jobs.db')
    conn.execute("""
        COPY search_result (id, url, search_terms, scrape_timestamp)
        FROM './data/results.csv' (delimiter '|', header true)
        ;
    """)
    return

if __name__ == '__main__':
    copy_search_results()