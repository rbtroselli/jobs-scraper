from .classes.posts_iterator import PostsIterator, load_posts_csv_to_db

def posts_to_csv():
    posts_iterator = PostsIterator()
    posts_iterator.scrape_posts()
    posts_iterator.save_posts_to_csv()
    return

def posts_to_db():
    load_posts_csv_to_db()
    return
