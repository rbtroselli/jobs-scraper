from .classes.results_iterator import ResultsIterator, load_results_csv_to_db

def results_to_csv():
    results_iterator = ResultsIterator()
    results_iterator.scrape_results()
    results_iterator.save_results_to_csv()
    return

def results_to_db():
    load_results_csv_to_db()
    return