# get all urls in a csv file, in a later step check if they are already in the db, and add to the db (with id, url, search term, insert date)
from results_iterator import ResultsIterator
from functions import execute_query
from queries import copy_search_results, insert_new_search_results, update_search_result_last_run

if __name__ == '__main__':
    # scrape results to csv
    results_iterator = ResultsIterator()
    results_iterator.scrape_results()
    results_iterator.save_results()
    # load csv to db
    execute_query(copy_search_results)
    execute_query(insert_new_search_results)   
    execute_query(update_search_result_last_run)
