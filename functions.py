# Browser driver not needed anymore, since we are using selenium-manager
# https://www.selenium.dev/blog/2022/introducing-selenium-manager/
from selenium import webdriver

def get_driver():
    """ Return a driver to use selenium """
    user_data_dir = './browser/user_data' # local data folder
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10) # ?
    return driver

def get_keywords_list():
    """ Return a list of keywords to search, taken from file """
    with open('search_terms.txt') as f:
        keywords_list = f.readlines()
    keywords_list = [x.strip().replace(' ','+') for x in keywords_list]
    print(keywords_list)    
    return keywords_list