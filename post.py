import time
# if class name has space, replace with . 

class Post:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.title = None
        self.content = None
        self.scrape()

    def scrape(self):
        self.driver.get(self.url)
        self.content = self.driver.find_element('id','jobDescriptionText').text
        self.title = self.driver.find_element('class name', 'icl-u-xs-mb--xs.icl-u-xs-mt--none.jobsearch-JobInfoHeader-title').text

        time.sleep(0.5)
        return

    def display(self):
        # Implement a method to display or print the post's information
        print(f'Title: {self.title}')
        print(f'Content: {self.content}')
        return