# Browser driver not needed anymore, since we are using selenium-manager
# https://www.selenium.dev/blog/2022/introducing-selenium-manager/
from selenium import webdriver
import duckdb

def get_driver():
    """ Return a driver to use selenium """
    user_data_dir = './browser/user_data' # local data folder
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10) # ?
    return driver

def get_search_terms_list():
    """ Return a list of search_terms to search, taken from file """
    with open('./data/search_terms.txt') as f:
        search_terms_list = f.readlines()
    search_terms_list = [x.strip().replace(' ','+') for x in search_terms_list]
    print(search_terms_list)    
    return search_terms_list

def execute_query(query):
    """ Execute a query on the db """
    conn = duckdb.connect('./data/jobs.db')
    conn.execute(query)
    return 