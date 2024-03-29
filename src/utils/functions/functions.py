# Browser driver not needed anymore, since we are using selenium-manager
# https://www.selenium.dev/blog/2022/introducing-selenium-manager/
import duckdb
import undetected_chromedriver as uc
# from selenium import webdriver

def _get_driver():
    """ Return a driver to use selenium """
    user_data_dir = './browser/user_data' # local data folder

    driver = uc.Chrome(headless=False, user_data_dir=user_data_dir)

    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # # headless
    # chrome_options.add_argument(f'--user-agent={user_agent}')
    # chrome_options.add_argument('--window-size=1920,1080')
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(10) # ?

    return driver

def _get_search_terms_list():
    """ Return a list of search_terms to search, taken from file """
    with open('./data/search_terms.txt') as f:
        search_terms_list = f.readlines()
    search_terms_list = [x.strip().replace(' ','+') for x in search_terms_list]
    print(search_terms_list)    
    return search_terms_list

def _execute_query(query):
    """ Execute a query on the db """
    conn = duckdb.connect('./data/jobs.db')
    conn.execute(query)
    return 

def _execute_query_get_df(query):
    """ Execute a query on the db and return df with records obtained """
    conn = duckdb.connect('./data/jobs.db')
    df = conn.query(query).to_df()
    return df
