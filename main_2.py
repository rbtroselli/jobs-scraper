# get all urls in a csv file, in a later step check if they are already in the db, and add to the db (with id, url, search term, insert date)
from results_iterator import ResultsIterator
from db_queries import copy_search_results

if __name__ == '__main__':
    results_iterator = ResultsIterator()
    results_iterator.scrape_results()
    results_iterator.save_results()
    copy_search_results()
