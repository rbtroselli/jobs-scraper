import time
import random 
from functions import get_driver
from search_page import SearchPage

# fermati quando becchi tutti url già visti?


driver = get_driver()
url = 'https://www.indeed.com/jobs?q=%22data+scientist%22&sort=date&filter=0&start=0'

search_page = SearchPage(url, driver)

search_page.display()

driver.quit()