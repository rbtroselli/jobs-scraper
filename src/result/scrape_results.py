from .classes.results_iterator import ResultsIterator
from ..utils.functions.functions import execute_query
from ..utils.queries.queries import insert_new_search_results

def run(last_3_days=False):
    # scrape results to csv
    results_iterator = ResultsIterator()
    results_iterator.scrape_results(last_3_days)
    results_iterator.save_results()
    # load csv to db
    execute_query(insert_new_search_results)
    return
