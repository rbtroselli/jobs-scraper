import time
import random
from result_page import ResultPage
from functions import get_driver, get_search_terms_list

class ResultsIterator:
    """ A class to iterate through the search results, combine all the pages and save them """
    def __init__(self):
        self.search_terms_list = get_search_terms_list()
        self.driver = get_driver()
        self.results_list = []
        return

    def _iterate_pages(self, search_terms):
        """ Iterate through the pages of a SINGLE SEARCH TERMS combo results """
        for i in range(0, 10000, 10):
            url = f'https://www.indeed.com/jobs?q=%22{search_terms}%22&sort=date&start={i}'
            result_page = ResultPage(url, self.driver, search_terms)
            result_page.display()
            local_results = result_page.get_results_dict_list()
            if all(result['id'] in [e['id'] for e in self.results_list] for result in local_results):
                break # if all results ids are already in results_list, break
            for result in local_results:
                self.results_list.append(result)
            time.sleep(random.uniform(5,15))
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
        return self.results_list
    
    def save_results(self):
        """ Save the results in a csv file """
        with open('results.csv','w') as f:
            f.write('id,url,search_terms,scrape_timestamp\n')
            for result in self.results_list:
                f.write(f"{result['id']},{result['url']},{result['search_terms']},{result['scrape_timestamp']}\n")
        return