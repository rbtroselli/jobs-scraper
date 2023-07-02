import time
import random 
from functions import get_driver, get_keywords_list
from result_page import ResultPage
from results_iterator import ResultsIterator

# fermati quando becchi tutti url già visti?
# get all urls in a csv file, in a later step check if they are already in the db, and add to the db (with id, url, search term, insert date)





if __name__ == '__main__':
    keywords_list = get_keywords_list()
    driver = get_driver()

    results_iterator = ResultsIterator(keywords_list, driver)
    results_iterator.get_posts_list()
    results_iterator.save_posts()
    
    driver.quit()