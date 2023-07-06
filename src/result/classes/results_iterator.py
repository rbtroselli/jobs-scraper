import time
import random
import pandas as pd
from .result_page import ResultPage
from ...utils.functions.functions import get_driver, get_search_terms_list

countries_dict = {
    'us':'', 'it':'it.', 'uk':'uk.', 'es':'es.', 'fr':'fr.', 'de':'de.', 'at':'at.', 'be':'be.', 
    'ca':'ca.', 'fi':'fi.', 'dk':'dk.', 'cz':'cz.', 'gr':'gr.', 'hu':'hu.', 'ie':'ie.', 'lu':'lu.', 
    'nl':'nl.', 'no':'no.', 'pl':'pl.', 'pt':'pt.', 'ro':'ro.', 'se':'se.', 'ch':'ch.', 'ua':'ua.', 
    'cn':'cn.', 'ar':'ar.', 'au':'au.', 'bh':'bh.', 'br':'br.', 'cl':'cl.', 'ch':'ch.', 'co':'co.', 
    'cr':'cr.', 'ec':'ec.', 'eg':'eg.', 'hk':'hk.', 'in':'in.', 'id':'id.', 'il':'il.', 'jp':'jp.', 
    'kw':'kw.', 'mx':'mx.', 'ma':'ma.', 'nz':'nz.', 'ng':'ng.', 'om':'om.', 'pk':'pk.', 'pa':'pa.', 
    'pe':'pe.', 'ph':'ph.', 'qa':'qa.', 'sa':'sa.', 'sg':'sg.', 'za':'za.', 'kr':'kr.', 'tw':'tw.', 
    'th':'th.', 'tr':'tr.', 'ae':'ae.', 'uy':'uy.', 've':'ve.', 'vn':'vn.', 'my':'malaysia.'
}


class ResultsIterator:
    """ A class to iterate through the search results, combine all the pages and save them """
    def __init__(self):
        self.search_terms_list = get_search_terms_list()
        self.driver = get_driver()
        self.results_list = []
        self.search_results_df = None
        self.last_3_days_string = None
        return
    
    def _make_search_results_df(self):
        """ Make a dataframe from the search_results list of dictionaries """
        self.search_results_df = pd.DataFrame(self.results_list, index=None)
        return
    
    def _deduplicate_search_results(self):
        """ Deduplicate repeated search results (encountered with different search terms) """
        self.search_results_df.drop_duplicates(subset=['id'], keep='first', inplace=True)
        return

    def _iterate_pages(self, search_terms, site_country):
        """ Iterate through the pages of a SINGLE SEARCH TERMS combo results """
        country_domain = countries_dict[site_country]
        for i in range(0, 10000, 10):
            url = f'https://{country_domain}indeed.com/jobs?q="{search_terms}"&sort=date{self.last_3_days_string}&start={i}'
            result_page = ResultPage(url, self.driver, search_terms, site_country)
            result_page.display()
            local_results = result_page.get_results_dict_list()
            if all(result['id'] in [e['id'] for e in self.results_list] for result in local_results):
                time.sleep(random.uniform(2,4))
                break # if all results ids are already in results_list, break
            for result in local_results:
                self.results_list.append(result)
            time.sleep(random.uniform(2,4))
        return
    
    def _iterate_countries(self, search_terms):
        # iterate countries keys
        for site_country in countries_dict.keys():
            self._iterate_pages(search_terms, site_country)
        return

    def _iterate_search_terms(self):
        """ Iterate through the search terms list """
        for search_terms in self.search_terms_list:
            self._iterate_countries(search_terms)
        self.driver.quit()
        return

    def scrape_results(self, last_3_days=True):
        """ Scrape and return the list of results """
        self.last_3_days_string = ('&fromage=3' if last_3_days is True else '')
        self._iterate_search_terms()
        self._make_search_results_df()
        self._deduplicate_search_results()
        return self.results_list, self.search_results_df
    
    def save_results(self):
        """ Save the results in a csv file """
        self.search_results_df.to_csv('./data/results.csv', sep='|', index=False)
        return
    