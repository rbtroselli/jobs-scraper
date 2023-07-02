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
        for i in range(0, 10000, 10):
            url = f'https://www.indeed.com/jobs?q=%22{keyword}%22&sort=date&start={i}'
            result_page = ResultPage(url, self.driver, keyword)
            result_page.display()
            posts = result_page.get_posts()
            if all(post['id'] in [e['id'] for e in self.posts_list] for post in posts):
                break # if all posts ids are already in posts_list, break
            for post in posts:
                self.posts_list.append(post)
            time.sleep(random.uniform(5,15))
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
    
    def save_posts(self):
        with open('posts.csv','w') as f:
            f.write('id,url,keyword,scrape_date\n')
            for post in self.posts_list:
                f.write(f"{post['id']},{post['url']},{post['keyword']},{post['scrape_date']}\n")
        return