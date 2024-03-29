import duckdb

conn = duckdb.connect('./data/jobs.db')

# to remove: varchar lengths, no needed in duckdb

# Getting current timestamp in UTC is surprisingly difficult
# the cast to varchar isolates the '+2' offset, the cast to timestamp renoves it
# conn.execute("""DROP TABLE IF EXISTS search_result""")
# conn.execute("""
#     CREATE TABLE IF NOT EXISTS search_result (
#         id VARCHAR,
#         url VARCHAR,
#         search_terms VARCHAR,
#         title VARCHAR,
#         site_country VARCHAR,
#         scrape_timestamp TIMESTAMP,
#         insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP::VARCHAR::TIMESTAMP 
#     )
# """)

# conn.execute("""DROP TABLE IF EXISTS post""")
# conn.execute("""
#     CREATE TABLE IF NOT EXISTS post (
#         id VARCHAR(16),
#         url VARCHAR(50),
#         search_terms VARCHAR(50),
#         site_country VARCHAR(2),
#         scrape_timestamp TIMESTAMP,
#         content VARCHAR(1000),
#         title VARCHAR(100),
#         posted_timestamp TIMESTAMP,
#         address_country VARCHAR(50),
#         address_locality VARCHAR(50),
#         address_region_0 VARCHAR(50),
#         address_region_1 VARCHAR(50),
#         address_region_2 VARCHAR(50),
#         postal_code VARCHAR(20),
#         hiring_organization VARCHAR(100),
#         country_requirements VARCHAR(50),
#         salary_currency VARCHAR(50),
#         min_salary FLOAT,
#         max_salary FLOAT,
#         salary FLOAT,
#         salary_unit VARCHAR(20),
#         job_location_type VARCHAR(50),
#         employment_type VARCHAR(50),
#         direct_apply BOOLEAN,
#         insert_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP::VARCHAR::TIMESTAMP 
#     )
# """)