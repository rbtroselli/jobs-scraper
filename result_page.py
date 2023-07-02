class ResultPage:
    """ A class to represent a result page, with post urls """
    def __init__(self, url, driver, keyword):
        self.url = url
        self.driver = driver
        self.posts = []
        self.keyword = keyword.replace('+',' ')
        self._scrape()
        return

    def _scrape(self):
        self.driver.get(self.url)
        posts = self.driver.find_elements('class name', 'jcs-JobTitle.css-jspxzf.eu4oa1w0')
        for post in posts:
            id = post.get_attribute('id').replace('job_','')
            self.posts.append({
                'id': id,
                'url': f'https://www.indeed.com/viewjob?jk={id}',
                'keyword': self.keyword
            })
        return
    
    def display(self):
        for post in self.posts:
            print(post['id'])
            print(post['url'])
            print(post['keyword'])
        return

    def get_posts(self):
        return self.posts