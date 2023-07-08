import time
import random
import pandas as pd
import os
from datetime import datetime
from .result_page import ResultPage
from ...utils.functions.functions import _get_driver, _get_search_terms_list, _execute_query
from ...utils.queries.queries import insert_new_search_results

countries_dict = {
    'US':'', 'IT':'it.', 'UK':'uk.', 'ES':'es.', 'FR':'fr.', 'DE':'de.', 'AT':'at.', 'BE':'be.', 
    'CA':'ca.', 'FI':'fi.', 'DK':'dk.', 'CZ':'cz.', 'GR':'gr.', 'HU':'hu.', 'IE':'ie.', 'LU':'lu.', 
    'NL':'nl.', 'NO':'no.', 'PL':'pl.', 'PT':'pt.', 'RO':'ro.', 'SE':'se.', 'CH':'ch.', 'UA':'ua.', 
    'CN':'cn.', 'AR':'ar.', 'AU':'au.', 'BH':'bh.', 'BR':'br.', 'CL':'cl.', 'CH':'ch.', 'CO':'co.', 
    'CR':'cr.', 'EC':'ec.', 'EG':'eg.', 'HK':'hk.', 'IN':'in.', 'ID':'id.', 'IL':'il.', 'JP':'jp.', 
    'KW':'kw.', 'MX':'mx.', 'MA':'ma.', 'NZ':'nz.', 'NG':'ng.', 'OM':'om.', 'PK':'pk.', 'PA':'pa.', 
    'PE':'pe.', 'PH':'ph.', 'QA':'qa.', 'SA':'sa.', 'SG':'sg.', 'ZA':'za.', 'KR':'kr.', 'TW':'tw.', 
    'TH':'th.', 'TR':'tr.', 'AE':'ae.', 'UY':'uy.', 'VE':'ve.', 'VN':'vn.', 'MY':'malaysia.'
}

results_csv = './data/results.csv'
results_csv_archived = './data/archive/results_{}.csv'


class ResultsIterator:
    """ A class to iterate through the search results, combine all the pages and save them """
    def __init__(self):
        self.search_terms_list = _get_search_terms_list()
        self.driver = _get_driver()
        self.results_list = []
        self.search_results_df = None
        self.last_3_days_string = None
        return
    
    def _make_search_results_df(self):
        """ Make a dataframe from the search_results list of dictionaries """
        self.search_results_df = pd.DataFrame(self.results_list, index=None)
        return
    
    def _deduplicate_search_results(self):
        """ Deduplicate repeated search results (results encountered with multiple search terms) """
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
                time.sleep(random.uniform(1.5,2.5))
                break # if all results ids are already in results_list, break
            for result in local_results:
                self.results_list.append(result)
            time.sleep(random.uniform(1.5,2.5))
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
    
    def save_results_to_csv(self):
        """ Save the results in a csv file. Raise error if the file already exists """
        if os.path.exists(results_csv):
            raise FileExistsError('The CSV already exists. Please load results and move it to archive')
        self.search_results_df.to_csv(results_csv, sep='|', index=False)
        return
    
def _move_results_csv_to_archive():
    """ Move results csv to archive """
    utc_ts = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S_UTC')
    os.rename(results_csv, results_csv_archived.format(utc_ts))
    return
    
def load_results_csv_to_db():
    """ Load posts csv to db """
    _execute_query(insert_new_search_results.format(results_csv))
    _move_results_csv_to_archive()
    return
    