from posts_iterator import PostsIterator

if __name__ == '__main__':
    posts_iterator = PostsIterator()
    posts_iterator.scrape_posts()
    posts_iterator.save_posts()
