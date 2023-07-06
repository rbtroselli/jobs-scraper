import duckdb

conn = duckdb.connect('./data/jobs.db')

# conn.execute("""DROP TABLE IF EXISTS raw_search_result""")
# conn.execute("""
#     CREATE TABLE IF NOT EXISTS raw_search_result (
#         id VARCHAR(16),
#         url VARCHAR(50),
#         search_terms VARCHAR(50),
#         scrape_timestamp TIMESTAMP,
#         insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# """)

# Getting current timestamp in UTC is surprisingly difficult
# the cast to varchar isolates the '+2' offset, the cast to timestamp renoves it
conn.execute("""DROP TABLE IF EXISTS search_result""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS search_result (
        id VARCHAR(16),
        url VARCHAR(50),
        search_terms VARCHAR(50),
        site_country VARCHAR(2),
        scrape_timestamp TIMESTAMP,
        insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP::VARCHAR::TIMESTAMP 
    )
""")
             
# conn.execute("""DROP TABLE IF EXISTS flow_step_cfg""")
# conn.execute("""
#     CREATE TABLE IF NOT EXISTS flow_step_cfg (
#         flow_step VARCHAR(20),
#         last_run_timestamp TIMESTAMP
#     )
# """)
# conn.execute("""
#     INSERT INTO flow_step_cfg (flow_step, last_run_timestamp)
#     VALUES ('search_result_load', '2023-01-01 00:00:00')
# """)

conn.execute("""DROP TABLE IF EXISTS post""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS post (
        id VARCHAR(16),
        url VARCHAR(50),
        search_terms VARCHAR(50),
        site_country VARCHAR(2),
        scrape_timestamp TIMESTAMP,
        content VARCHAR(1000),
        title VARCHAR(100),
        posted_timestamp TIMESTAMP,
        address_country VARCHAR(50),
        address_locality VARCHAR(50),
        address_region_0 VARCHAR(50),
        address_region_1 VARCHAR(50),
        address_region_2 VARCHAR(50),
        postal_code VARCHAR(20),
        hiring_organization VARCHAR(100),
        country_requirements VARCHAR(50),
        salary_currency VARCHAR(50),
        min_salary FLOAT,
        max_salary FLOAT,
        salary_unit VARCHAR(20),
        job_location_type VARCHAR(50),
        employment_type VARCHAR(50),
        valid_through_timestamp TIMESTAMP,
        direct_apply BOOLEAN,
        raw_script_json VARCHAR(1000),
        insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP::VARCHAR::TIMESTAMP 
    )
""")
# conn.execute("""
#     INSERT INTO flow_step_cfg (flow_step, last_run_timestamp)
#     VALUES ('post_load', '2023-01-01 00:00:00')
# """)  