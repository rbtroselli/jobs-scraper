from selenium import webdriver

def get_driver():
    # assign driver path and get user data into a local folder
    chrome_driver_path='./browser/chromedriver'
    user_data_dir = './browser/user_data'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    # chrome_options.binary_location = './browser/chrome.app' # use standalone chrome app

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.implicitly_wait(10) # ?
    return driver