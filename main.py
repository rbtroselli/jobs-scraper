import sys
from src.result.scrape_results import results_to_csv, results_to_db
from src.post.scrape_posts import posts_to_csv, posts_to_db


if __name__ == '__main__':
    valid_args = ['scrape_results', 'load_results', 'scrape_posts', 'load_posts', 'results', 'posts', 'all']
    args = sys.argv[1:]

    # check if any arguments are given
    if len(args) < 1:
        print(f'Give one or more valid arguments: {valid_args}')
        sys.exit(1)
    # check if any of the arguments are not valid
    if any(arg not in valid_args for arg in args):
        print(f'Give one or more valid arguments: {valid_args}')
        sys.exit(1)

    if 'all' in args:
        results_to_csv()
        results_to_db()
        posts_to_csv()
        posts_to_db()
        sys.exit(0)
    
    if 'results' in args:
        results_to_csv()
        results_to_db()
        sys.exit(0)
    
    if 'posts' in args:
        posts_to_csv()
        posts_to_db()
        sys.exit(0)
    
    if 'scrape_results' in args:
        results_to_csv()
    if 'load_results' in args:
        results_to_db()
    if 'scrape_posts' in args:
        posts_to_csv()
    if 'load_posts' in args:
        posts_to_db()
    sys.exit(0)
