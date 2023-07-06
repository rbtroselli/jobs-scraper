import time
import random
import pandas as pd
from .result_page import ResultPage
from ...utils.functions.functions import get_driver, get_search_terms_list

class ResultsIterator:
    """ A class to iterate through the search results, combine all the pages and save them """
    def __init__(self):
        self.search_terms_list = get_search_terms_list()
        self.driver = get_driver()
        self.results_list = []
        self.search_results_df = None
        return
    
    def _make_search_results_df(self):
        """ Make a dataframe from the search_results list of dictionaries """
        self.search_results_df = pd.DataFrame(self.results_list, index=None)
        return
    
    def _deduplicate_search_results(self):
        """ Deduplicate repeated search results (encountered with different search terms) """
        self.search_results_df.drop_duplicates(subset=['id'], keep='first', inplace=True)
        return

    def _iterate_pages(self, search_terms):
        """ Iterate through the pages of a SINGLE SEARCH TERMS combo results """
        for i in range(0, 10000, 10):
            url = f'https://indeed.com/jobs?q=%22{search_terms}%22&sort=date&start={i}'
            result_page = ResultPage(url, self.driver, search_terms)
            result_page.display()
            local_results = result_page.get_results_dict_list()
            if all(result['id'] in [e['id'] for e in self.results_list] for result in local_results):
                break # if all results ids are already in results_list, break
            for result in local_results:
                self.results_list.append(result)
            time.sleep(random.uniform(3,5))
        return

    def _iterate_search_terms(self):
        """ Iterate through the search terms list """
        for search_terms in self.search_terms_list:
            self._iterate_pages(search_terms)
        self.driver.quit()
        return

    def scrape_results(self):
        """ Scrape and return the list of results """
        self._iterate_search_terms()
        self._make_search_results_df()
        self._deduplicate_search_results()
        return self.results_list, self.search_results_df
    
    def save_results(self):
        """ Save the results in a csv file """
        self.search_results_df.to_csv('./data/results.csv', sep='|', index=False)
        return
    