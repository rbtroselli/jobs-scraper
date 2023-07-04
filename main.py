from posts_iterator import PostsIterator
from functions import execute_query
from queries import copy_posts, update_posts_last_run

if __name__ == '__main__':
    # scrape posts to csv
    posts_iterator = PostsIterator()
    posts_iterator.scrape_posts()
    posts_iterator.save_posts()
    # load csv to db
    execute_query(copy_posts)
    # execute_query(update_posts_last_run)
