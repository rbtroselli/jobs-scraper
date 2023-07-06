from ...utils.functions.functions import get_driver
from ...utils.queries.queries import get_search_results_to_scrape
from .post import Post
import pandas as pd
import time 
import random
import duckdb


class PostsIterator:
    """ 
    A class to iterate through posts, combine all the posts and save them.
    Takes in input the list of the posts from the db. Using pandas because of structured data 
    """
    def __init__(self):
        self.driver = get_driver()
        self.conn = duckdb.connect('./data/jobs.db')
        self.results_df = None
        self.posts_list = []
        self.posts_df = None
        self._get_results_df()
        return
    
    def _get_results_df(self):
        """ Get the results dataframe from the db """
        self.results_df = self.conn.query(get_search_results_to_scrape).to_df()
        return
    
    def _make_posts_df(self):
        """ Make a dataframe from the posts list of dictionaries """
        self.posts_df = pd.DataFrame(self.posts_list, index=None)
        return
    
    def _remove_separator_from_df(self):
        """ Remove the CSV separator from everywhere in the dataframe """
        self.posts_df.replace('\|', '-', regex=True, inplace=True)
        return

    def _iterate_posts(self):
        """ Iterate through the posts (results), add their data dict to the posts list """
        for index, row in self.results_df.iterrows():
            url = row['url']
            id = row['id']
            search_terms = row['search_terms']
            site_country = row['site_country']
            # scrape_timestamp = row['scrape_timestamp'] # not needed for post
            post = Post(url, id, search_terms, site_country, self.driver)
            post.display()
            self.posts_list.append(post.get_post_dict())
            time.sleep(random.uniform(2,4))
        self.driver.quit()
        return
    
    def scrape_posts(self):
        """ Scrape and return the list of posts and posts df """
        self._iterate_posts()
        self._make_posts_df()
        self._remove_separator_from_df()
        return self.posts_list, self.posts_df
    
    def save_posts(self):
        """ Save the posts in a csv file """
        self.posts_df.to_csv('./data/posts.csv', sep='|', index=False)
        return
