import time
import random
from result_page import ResultPage

class ResultsIterator:
    """ A class to iterate through the search results, save and eventually return a list of posts urls """
    def __init__(self, search_terms_list, driver):
        self.search_terms_list = search_terms_list
        self.driver = driver
        self.posts_list = []

    def _iterate_pages(self, search_terms):
        """ Iterate through the pages of a SINGLE SEARCH TERMS combo results """
        for i in range(0, 10000, 10):
            url = f'https://www.indeed.com/jobs?q=%22{search_terms}%22&sort=date&start={i}'
            result_page = ResultPage(url, self.driver, search_terms)
            result_page.display()
            posts = result_page.get_results_list()
            if all(post['id'] in [e['id'] for e in self.posts_list] for post in posts):
                break # if all posts ids are already in posts_list, break
            for post in posts:
                self.posts_list.append(post)
            time.sleep(random.uniform(5,15))
        return

    def _iterate_search_terms(self):
        """ Iterate through the search terms list """
        for search_terms in self.search_terms_list:
            self._iterate_pages(search_terms)
        return

    def scrape_results(self):
        """ Return the list of posts """
        self._iterate_search_terms()
        return self.posts_list
    
    def save_posts(self):
        with open('posts.csv','w') as f:
            f.write('id,url,search_terms,scrape_timestamp\n')
            for post in self.posts_list:
                f.write(f"{post['id']},{post['url']},{post['search_terms']},{post['scrape_timestamp']}\n")
        return