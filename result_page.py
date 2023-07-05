from datetime import datetime

class ResultPage:
    """ A class to represent a result page, with post urls """
    def __init__(self, url, driver, search_terms):
        self.url = url
        self.driver = driver
        self.results_list = []
        self.search_terms = search_terms.replace('+',' ')
        self.scrape_timestamp = datetime.now()
        self._scrape()
        return

    def _scrape(self):
        self.driver.get(self.url)
        raw_results = self.driver.find_elements('class name', 'jcs-JobTitle.css-jspxzf.eu4oa1w0')
        for raw_result in raw_results:
            id = raw_result.get_attribute('data-jk')
            self.results_list.append({
                'id': id,
                'url': f'https://www.indeed.com/viewjob?jk={id}',
                'search_terms': self.search_terms,
                'scrape_timestamp': self.scrape_timestamp
            })
        return
    
    def display(self):
        for result in self.results_list:
            for key, value in result.items():
                print(f'{key}: {value}')
        return

    def get_results_dict_list(self):
        return self.results_list
