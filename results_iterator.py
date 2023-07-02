import time
import random
from result_page import ResultPage

class ResultsIterator:
    """ A class to iterate through the search results, save and eventually return a list of posts urls """
    def __init__(self, keywords_list, driver):
        self.keywords_list = keywords_list
        self.driver = driver
        self.posts_list = []

    def _iterate_pages(self, keyword):
        """ Iterate through the pages of a SINGLE KEYWORDS search results """
        for i in range(0, 20, 10):
            url = f'https://www.indeed.com/jobs?q=%22{keyword}%22&sort=date&filter=0&start={i}'
            result_page = ResultPage(url, self.driver, keyword)
            result_page.display()
            posts = result_page.get_posts()
            for post in posts:
                self.posts_list.append(post)
            time.sleep(random.uniform(5,10))
        return

    def _iterate_keywords(self):
        """ Iterate through the keywords list """
        for keyword in self.keywords_list:
            self._iterate_pages(keyword)
        return

    def get_posts_list(self):
        """ Return the list of posts """
        self._iterate_keywords()
        return self.posts_list