# classe, ha un attributo che è la lista degli url, che ritorna scrapati al main, che li checka contro un db e li aggiunge se mancano

class SearchPage:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.posts = []
        self.search_term = ''


        self.scrape()
        return

    def scrape(self):
        self.driver.get(self.url)


        posts = self.driver.find_elements('class name', 'jcs-JobTitle.css-jspxzf.eu4oa1w0')
        for post in posts:
            id = post.get_attribute('id').replace('job_','')
            self.posts.append({
                'id': id,
                'url': f'https://www.indeed.com/viewjob?jk={id}'
            })
        return
    
    def display(self):
        for post in self.posts:
            print(post['id'])
            print(post['url'])
        return