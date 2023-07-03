import duckdb

# create a db
conn = duckdb.connect('./data/jobs.db')

# conn.execute("""DROP TABLE IF EXISTS search_result""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS search_result (
        id VARCHAR(16),
        url VARCHAR(50),
        search_terms VARCHAR(50),
        scrape_timestamp TIMESTAMP,
        insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")