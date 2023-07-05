# leaner approach: no cfg
# make process leaner and storage lighter by loading only new results (insert into, not copy)
insert_new_search_results = """
    INSERT INTO search_result (id, url, search_terms, scrape_timestamp)
    SELECT id, url, search_terms, scrape_timestamp
    FROM read_csv('./data/results.csv', delim='|', header=true, auto_detect=true)
    WHERE id NOT IN (SELECT id FROM search_result)
    ;
"""
get_search_results_to_scrape = """
    SELECT id, url, search_terms
    FROM search_result
    WHERE id NOT IN (SELECT id FROM post)
    ;
"""
insert_new_posts = """
    INSERT INTO post (id, url, search_terms, scrape_timestamp, content, title, posted_date, address_country, 
        address_locality, address_region_0, address_region_1, address_region_2, postal_code, hiring_organization, 
        country_requirements, salary_currency, min_salary, max_salary, salary_unit, job_location_type, 
        employment_type, valid_through_date, direct_apply, raw_script_json)
    SELECT *
    FROM read_csv_auto('./data/posts.csv', delimiter='|', header=true)
    WHERE id NOT IN (SELECT id FROM post)
"""

'''
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
        insert_update_timestamp > (SELECT last_run_timestamp FROM flow_step_cfg WHERE step='search_result_load')
        AND id NOT IN (SELECT id FROM search_result)
    ;
"""
update_search_results_last_run = """
    UPDATE flow_step_cfg
    SET last_run_timestamp = CURRENT_TIMESTAMP
    WHERE source='raw_search_result'
    ;
"""

# search results to scrape
get_search_results_to_scrape = """
    SELECT id, url, search_terms
    FROM search_result
    WHERE insert_update_timestamp > (SELECT last_run_timestamp FROM flow_step_cfg WHERE flow_step='post_load')
    ;
"""

# posts
copy_posts = """
    COPY post (id, url, search_terms, scrape_timestamp, content, title, posted_date, address_country, 
        address_locality, address_region_0, address_region_1, address_region_2, postal_code, hiring_organization, 
        country_requirements, salary_currency, min_salary, max_salary, salary_unit, job_location_type, 
        employment_type, valid_through_date, direct_apply, raw_script_json)
    FROM './data/posts.csv' (delimiter '|', header true)
    ;
"""

update_posts_last_run = """
    UPDATE flow_step_cfg
    SET last_run_timestamp = CURRENT_TIMESTAMP
    WHERE flow_step='post_load'
    ;
"""
'''