import json
from datetime import datetime


class Post:
    """ A class to represent a single job post """
    def __init__(self, url, id, search_terms, driver):
        self.url = url
        self.id = id
        self.search_terms = search_terms
        self.driver = driver
        self.scrape_timestamp = datetime.now()
        self.title = None
        self.content = None
        self.company = None
        self.posted_date = None
        # location
        self.address_country = None
        self.address_locality = None
        self.address_region_0 = None
        self.address_region_1 = None
        self.address_region_2 = None
        self.postal_code = None
        # hiring organization
        self.hiring_organization = None
        # location requirements
        self.country_requirements = None
        # salary
        self.min_salary = None
        self.max_salary = None
        self.salary_currency = None
        self.salary_unit = None
        # other
        self.job_location_type = None
        self.employment_type = None
        self.valid_through_date = None
        self.direct_apply = None
        self.title_again = None
        self.raw_script_json = None
        self._scrape()
        return

    def _scrape(self):
        """ Scrape the job post """
        self.driver.get(self.url)
        # replace space in class names with dots
        self.title = self.driver.find_element('class name', 'icl-u-xs-mb--xs.icl-u-xs-mt--none.jobsearch-JobInfoHeader-title').text
        self.content = self.driver.find_element('id','jobDescriptionText').text.replace('\n',' ')
        self.company = self.driver.find_element('class name', 'css-1cjkto6.eu4oa1w0').text
        # dict.get(key,alternative) returns alternative if it cant find key. fail safe
        script_json = self.driver.find_element('xpath', "//script[@type = 'application/ld+json']").get_attribute('innerHTML')
        script_dict = json.loads(script_json)
        self.posted_date = script_dict.get('datePosted','').split('T')[0]
        # location
        self.address_country = script_dict.get('jobLocation','').get('address','').get('addressCountry','')
        self.address_locality = script_dict.get('jobLocation','').get('address','').get('addressLocality','')
        self.address_region_0 = script_dict.get('jobLocation','').get('address','').get('addressRegion','')
        self.address_region_1 = script_dict.get('jobLocation','').get('address','').get('addressRegion1','')
        self.address_region_2 = script_dict.get('jobLocation','').get('address','').get('addressRegion2','')
        self.postal_code = script_dict.get('jobLocation','').get('address','').get('postalCode','')
        # hiring organization
        self.hiring_organization = script_dict.get('hiringOrganization','').get('name','')
        # location requirements
        try:
            self.country_requirements = script_dict.get('applicantLocationRequirements','').get('name','')
        except:
            pass
        # salary
        try:
            self.salary_currency = script_dict.get('baseSalary','').get('currency','')
            self.min_salary = script_dict.get('baseSalary','').get('value','').get('minValue','')
            self.max_salary = script_dict.get('baseSalary','').get('value','').get('maxValue','')
            self.salary_unit = script_dict.get('baseSalary','').get('value','').get('unitText','')
        except:
            pass
        # other
        self.job_location_type = script_dict.get('jobLocationType','')
        self.employment_type = script_dict.get('employmentType','')
        self.valid_through_date = script_dict.get('validThrough','').split('T')[0]
        self.direct_apply = script_dict.get('directApply','')
        self.title_again = script_dict.get('title','')
        self.raw_script_json = str(script_json)
        return

    def display(self):
        print('-----------------')
        print(f'URL: {self.url}')
        print(f'ID: {self.id}')
        print(f'Search Terms: {self.search_terms}')
        print(f'Scrape Timestamp: {self.scrape_timestamp}')
        print(f'Title: {self.title}')
        print(f'Company: {self.company}')
        print(f'Posted Date: {self.posted_date}')
        # location
        print(f'Address Country: {self.address_country}')
        print(f'Address Locality: {self.address_locality}')
        print(f'Address Region 0: {self.address_region_0}')
        print(f'Address Region 1: {self.address_region_1}')
        print(f'Address Region 2: {self.address_region_2}')
        print(f'Postal Code: {self.postal_code}')
        # hiring organization
        print(f'Hiring Organization: {self.hiring_organization}')
        # location requirements
        print(f'Country Requirements: {self.country_requirements}')
        # salary
        print(f'Salary Currency: {self.salary_currency}')
        print(f'Min Salary: {self.min_salary}')
        print(f'Max Salary: {self.max_salary}')
        print(f'Salary Unit: {self.salary_unit}')
        # other stuff
        print(f'Job Location Type: {self.job_location_type}')
        print(f'Employment Type: {self.employment_type}')
        print(f'Valid Through Date: {self.valid_through_date}')
        print(f'Direct Apply: {self.direct_apply}')
        print(f'Title Again: {self.title_again}')
        print(f'Content: {self.content[:100]}...')
        print(f'Raw Script Json: {self.raw_script_json[:100]}...')
        print('-----------------')
        return
    
    def get_post_dict(self):
        return {
            'url': self.url,
            'id': self.id,
            'search_terms': self.search_terms,
            'scrape_timestamp': self.scrape_timestamp,
            'title': self.title,
            'company': self.company,
            'posted_date': self.posted_date,
            # location
            'address_country': self.address_country,
            'address_locality': self.address_locality,
            'address_region_0': self.address_region_0,
            'address_region_1': self.address_region_1,
            'address_region_2': self.address_region_2,
            'postal_code': self.postal_code,
            # hiring organization
            'hiring_organization': self.hiring_organization,
            # location requirements
            'country_requirements': self.country_requirements,
            # salary
            'salary_currency': self.salary_currency,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'salary_unit': self.salary_unit,
            # other stuff
            'job_location_type': self.job_location_type,
            'employment_type': self.employment_type,
            'valid_through_date': self.valid_through_date,
            'direct_apply': self.direct_apply,
            'title_again': self.title_again,
            'content': self.content,
            'raw_script_json': self.raw_script_json
        }