from .classes.posts_iterator import PostsIterator
from ..utils.functions.functions import execute_query
from ..utils.queries.queries import insert_new_posts

def run():
    # scrape posts to csv
    posts_iterator = PostsIterator()
    posts_iterator.scrape_posts()
    posts_iterator.save_posts()
    # load csv to db
    execute_query(insert_new_posts)
    return
