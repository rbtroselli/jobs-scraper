# search results
copy_search_results = """
    COPY raw_search_result (id, url, search_terms, scrape_timestamp)
    FROM './data/results.csv' (delimiter '|', header true)
    ;
"""
insert_new_search_results = """
    INSERT INTO search_result (id, url, search_terms, scrape_timestamp)
    SELECT id, url, search_terms, scrape_timestamp
    FROM raw_search_result
    WHERE 
        insert_update_timestamp > (SELECT last_run_timestamp FROM flow_run_cfg WHERE source='raw_search_result')
        AND id NOT IN (SELECT id FROM search_result)
    ;
"""
update_search_result_last_run = """
    UPDATE flow_run_cfg
    SET last_run_timestamp = CURRENT_TIMESTAMP
    WHERE source='raw_search_result'
    ;
"""

# posts
copy_posts = """

"""
insert_new_posts = """

"""
update_posts_last_run = """

"""