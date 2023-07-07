from src.result.scrape_results import results_to_csv, results_to_db
from src.post.scrape_posts import posts_to_csv, posts_to_db

if __name__ == '__main__':
    if input('Scrape results? (y/n): ') == 'y':
       results_to_csv() 
    if input('Load results to db? (y/n): ')== 'y':
        results_to_db
    if input('Scrape posts? (y/n): ') == 'y':
        posts_to_csv()
    if input('Load posts to db? (y/n): ')== 'y':
        results_to_db
