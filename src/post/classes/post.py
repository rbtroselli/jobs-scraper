import json
from datetime import datetime


class Post:
    """ A class to represent a single job post """
    def __init__(self, url, id, search_terms, site_country, driver):
        self.post_dict = {}
        self.post_dict['id'] = id
        self.post_dict['url'] = url
        self.post_dict['search_terms'] = search_terms
        self.post_dict['site_country'] = site_country
        self.post_dict['scrape_timestamp'] = datetime.utcnow()
        self.driver = driver
        self._assign_post_elements()
        return

    def _scrape(self):
        """ Scrape the job post """
        self.driver.get(self.post_dict['url'])
        # replace space in class names with dots
        self.post_dict['content'] = self.driver.find_element('id','jobDescriptionText').text #.replace('\n',' ').replace('\r', ' ')
        # dict.get(key,alternative) returns alternative if it cant find key. fail safe
        script_json = self.driver.find_element('xpath', "//script[@type = 'application/ld+json']").get_attribute('innerHTML')
        script_dict = json.loads(script_json)
        self.post_dict['title'] = script_dict.get('title', None)
        self.post_dict['posted_timestamp'] = script_dict.get('datePosted', None)
        self.post_dict['address_country'] = script_dict.get('jobLocation', None).get('address', None).get('addressCountry', None)
        self.post_dict['address_locality'] = script_dict.get('jobLocation', None).get('address', None).get('addressLocality', None)
        self.post_dict['address_region_0'] = script_dict.get('jobLocation', None).get('address', None).get('addressRegion', None)
        self.post_dict['address_region_1'] = script_dict.get('jobLocation', None).get('address', None).get('addressRegion1', None)
        self.post_dict['address_region_2'] = script_dict.get('jobLocation', None).get('address', None).get('addressRegion2', None)
        self.post_dict['postal_code'] = script_dict.get('jobLocation', None).get('address', None).get('postalCode', None)
        self.post_dict['hiring_organization'] = script_dict.get('hiringOrganization', None).get('name', None)
        try:
            self.post_dict['country_requirements'] = script_dict.get('applicantLocationRequirements', None).get('name', None)
        except:
            pass
        try:
            self.post_dict['salary_currency'] = script_dict.get('baseSalary', None).get('currency', None)
            self.post_dict['min_salary'] = script_dict.get('baseSalary', None).get('value', None).get('minValue', None)
            self.post_dict['max_salary'] = script_dict.get('baseSalary', None).get('value', None).get('maxValue', None)
            self.post_dict['salary'] = script_dict.get('baseSalary', None).get('value', None).get('value', None)
            self.post_dict['salary_unit'] = script_dict.get('baseSalary', None).get('value', None).get('unitText', None)
        except:
            pass
        self.post_dict['job_location_type'] = script_dict.get('jobLocationType', None)
        self.post_dict['employment_type'] = script_dict.get('employmentType', None)
        self.post_dict['valid_through_timestamp'] = script_dict.get('validThrough', None)
        self.post_dict['direct_apply'] = script_dict.get('directApply', None)
        # self.post_dict['raw_script_json'] = str(script_json)
        return
    
    def _assign_post_elements(self):
        try:
            self._scrape()
        except:
            pass
        return

    def display(self):
        print('-'*100)
        for key, value in self.post_dict.items():
            if key == 'content':
                print(f'{key}: {value[0:100]}...')
            # elif key == 'raw_script_json':
            #     print(f'{key}: {value[0:100]}...')
            else:
                print(f'{key}: {value}')
        return
    
    def get_post_dict(self):
        return self.post_dict