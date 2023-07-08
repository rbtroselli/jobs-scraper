import pandas as pd
import time 
import random
import os
from datetime import datetime
from .post import Post
from ...utils.functions.functions import _get_driver, _execute_query_get_df, _execute_query
from ...utils.queries.queries import get_search_results_to_scrape, insert_new_posts

posts_csv = './data/posts.csv'
posts_csv_archived = './data/archive/posts_{}.csv'


class PostsIterator:
    """ 
    A class to iterate through posts, combine all the posts and save them.
    Takes in input the list of the posts from the db. Using pandas because of structured data 
    """
    def __init__(self):
        self.driver = _get_driver()
        # self.conn = duckdb.connect('./data/jobs.db')
        self.results_df = None
        self.posts_list = []
        self.posts_df = None
        self._get_results_df()
        return
    
    def _get_results_df(self):
        """ Get the results dataframe from the db """
        self.results_df = _execute_query_get_df(get_search_results_to_scrape)
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
            url, id, search_terms, site_country = row['url'], row['id'], row['search_terms'], row['site_country']
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
    
    def save_posts_to_csv(self):
        """ Save the posts in a csv file. Raise error if the file already exists """
        if os.path.exists(posts_csv):
            raise FileExistsError('The CSV already exists. Please load results and move it to archive')
        self.posts_df.to_csv(posts_csv, sep='|', index=False)
        return
    
def _move_posts_csv_to_archive():
    """ Move results csv to archive """
    utc_ts = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S_UTC')
    os.rename(posts_csv, posts_csv_archived.format(utc_ts))
    return
    
def load_posts_csv_to_db():
    """ Load posts csv to db """
    _execute_query(insert_new_posts.format(posts_csv))
    _move_posts_csv_to_archive()
    return

