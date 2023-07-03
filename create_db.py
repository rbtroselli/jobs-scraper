import duckdb

conn = duckdb.connect('./data/jobs.db')

conn.execute("""DROP TABLE IF EXISTS raw_search_result""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS raw_search_result (
        id VARCHAR(16),
        url VARCHAR(50),
        search_terms VARCHAR(50),
        scrape_timestamp TIMESTAMP,
        insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
             
conn.execute("""DROP TABLE IF EXISTS search_result""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS search_result (
        id VARCHAR(16),
        url VARCHAR(50),
        search_terms VARCHAR(50),
        scrape_timestamp TIMESTAMP,
        insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
             
conn.execute("""DROP TABLE IF EXISTS flow_run_cfg""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS flow_run_cfg (
        source VARCHAR(20),
        destination VARCHAR(20),
        last_run_timestamp TIMESTAMP,
        insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.execute("""
    INSERT INTO flow_run_cfg (source, destination, last_run_timestamp)
    VALUES ('raw_search_result', 'search_result', '2023-01-01 00:00:00')
""")
             