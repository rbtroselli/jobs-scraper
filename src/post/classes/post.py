import json
from datetime import datetime


class Post:
    """ A class to represent a single job post """
    def __init__(self, url, id, search_terms, driver):
        self.post_dict = {}
        self.post_dict['id'] = id
        self.post_dict['url'] = url
        self.post_dict['search_terms'] = search_terms
        self.post_dict['scrape_timestamp'] = datetime.now()
        self.driver = driver
        self._scrape()
        return

    def _scrape(self):
        """ Scrape the job post """
        self.driver.get(self.post_dict['url'])
        # replace space in class names with dots
        self.post_dict['content'] = self.driver.find_element('id','jobDescriptionText').text.replace('\n',' ')
        # dict.get(key,alternative) returns alternative if it cant find key. fail safe
        script_json = self.driver.find_element('xpath', "//script[@type = 'application/ld+json']").get_attribute('innerHTML')
        script_dict = json.loads(script_json)
        self.post_dict['title'] = script_dict.get('title','')
        self.post_dict['posted_date'] = script_dict.get('datePosted','').split('T')[0]
        self.post_dict['address_country'] = script_dict.get('jobLocation','').get('address','').get('addressCountry','')
        self.post_dict['address_locality'] = script_dict.get('jobLocation','').get('address','').get('addressLocality','')
        self.post_dict['address_region_0'] = script_dict.get('jobLocation','').get('address','').get('addressRegion','')
        self.post_dict['address_region_1'] = script_dict.get('jobLocation','').get('address','').get('addressRegion1','')
        self.post_dict['address_region_2'] = script_dict.get('jobLocation','').get('address','').get('addressRegion2','')
        self.post_dict['postal_code'] = script_dict.get('jobLocation','').get('address','').get('postalCode','')
        self.post_dict['hiring_organization'] = script_dict.get('hiringOrganization','').get('name','')
        try:
            self.post_dict['country_requirements'] = script_dict.get('applicantLocationRequirements','').get('name','')
        except:
            self.post_dict['country_requirements'] = None
        try:
            self.post_dict['salary_currency'] = script_dict.get('baseSalary','').get('currency','')
            self.post_dict['min_salary'] = script_dict.get('baseSalary','').get('value','').get('minValue','')
            self.post_dict['max_salary'] = script_dict.get('baseSalary','').get('value','').get('maxValue','')
            self.post_dict['salary_unit'] = script_dict.get('baseSalary','').get('value','').get('unitText','')
        except:
            self.post_dict['salary_currency'] = None
            self.post_dict['min_salary'] = None
            self.post_dict['max_salary'] = None
            self.post_dict['salary_unit'] = None
        self.post_dict['job_location_type'] = script_dict.get('jobLocationType','')
        self.post_dict['employment_type'] = script_dict.get('employmentType','')
        self.post_dict['valid_through_date'] = script_dict.get('validThrough','').split('T')[0]
        self.post_dict['direct_apply'] = script_dict.get('directApply','')
        self.post_dict['raw_script_json'] = str(script_json)
        return

    def display(self):
        for key, value in self.post_dict.items():
            if key == 'content':
                print(f'{key}: {value[0:100]}...')
            elif key == 'raw_script_json':
                print(f'{key}: {value[0:100]}...')
            else:
                print(f'{key}: {value}')
        return
    
    def get_post_dict(self):
        return self.post_dict