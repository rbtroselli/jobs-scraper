from post import Post
from selenium import webdriver
import time

def get_driver():
    chrome_driver_path='./browser/chromedriver'
    user_data_dir = './browser/user_data'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    # chrome_options.binary_location = './browser/chrome.app'

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.implicitly_wait(1)

    return driver



url = 'https://www.indeed.com/viewjob?jk=36910c9a332adba3&tk=1h48nq7efkefv800&from=serp&vjs=3'
driver = get_driver()

post = Post(url, driver)
post.display()

# gestire qui il csv, piazzarci la roba dell'oggetto post

# Close the browser
driver.quit()



