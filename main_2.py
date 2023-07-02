from functions import get_driver, get_search_terms_list
from results_iterator import ResultsIterator

# get all urls in a csv file, in a later step check if they are already in the db, and add to the db (with id, url, search term, insert date)





if __name__ == '__main__':
    search_terms_list = get_search_terms_list()
    driver = get_driver()

    results_iterator = ResultsIterator(search_terms_list, driver)
    results_iterator.scrape_results()
    results_iterator.save_posts()

    driver.quit()