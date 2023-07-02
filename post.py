import json
from datetime import date


class Post:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.scrape_date = date.today()
        self.title = None
        self.content = None
        self.company = None
        self.date_posted = None
        # location
        self.raw_job_location = None
        self.address_country = None
        self.address_locality = None
        self.address_region_0 = None
        self.address_region_1 = None
        self.address_region_2 = None
        self.postal_code = None
        # hiring organization
        self.raw_hiring_organization = None
        self.hiring_organization = None
        # location requirements
        self.raw_location_requirements = None
        self.country_requirements = None
        # salary
        self.raw_base_salary = None
        self.min_salary = None
        self.max_salary = None
        self.salary_currency = None
        self.salary_unit = None
        # other
        self.job_location_type = None
        self.employment_type = None
        self.valid_through = None
        self.direct_apply = None
        self.title_again = None
        self.raw_script_json = None
        self.scrape()
        return

    def scrape(self):
        self.driver.get(self.url)
        # replace space in class names with dots
        self.title = self.driver.find_element('class name', 'icl-u-xs-mb--xs.icl-u-xs-mt--none.jobsearch-JobInfoHeader-title').text
        self.content = self.driver.find_element('id','jobDescriptionText').text.replace('\n',' ')
        self.company = self.driver.find_element('class name', 'css-1cjkto6.eu4oa1w0').text
        # dict.get(key,alternative) returns alternative if it cant find key. fail safe
        script_json = self.driver.find_element_by_xpath("//script[@type = 'application/ld+json']").get_attribute('innerHTML')
        stuff_dict = json.loads(script_json)
        self.date_posted = stuff_dict.get('datePosted','').split('T')[0]
        # location
        self.raw_job_location = stuff_dict.get('jobLocation','')
        self.address_country = stuff_dict.get('jobLocation','').get('address','').get('addressCountry','')
        self.address_locality = stuff_dict.get('jobLocation','').get('address','').get('addressLocality','')
        self.address_region_0 = stuff_dict.get('jobLocation','').get('address','').get('addressRegion','')
        self.address_region_1 = stuff_dict.get('jobLocation','').get('address','').get('addressRegion1','')
        self.address_region_2 = stuff_dict.get('jobLocation','').get('address','').get('addressRegion2','')
        self.postal_code = stuff_dict.get('jobLocation','').get('address','').get('postalCode','')
        # hiring organization
        self.raw_hiring_organization = stuff_dict.get('hiringOrganization','')
        self.hiring_organization = stuff_dict.get('hiringOrganization','').get('name','')
        # location requirements
        try:
            self.raw_location_requirements = stuff_dict.get('applicantLocationRequirements','')
            self.country_requirements = stuff_dict.get('applicantLocationRequirements','').get('name','')
        except:
            pass
        # salary
        try:
            self.raw_base_salary = stuff_dict.get('baseSalary','')
            self.salary_currency = stuff_dict.get('baseSalary','').get('currency','')
            self.min_salary = stuff_dict.get('baseSalary','').get('value','').get('minValue','')
            self.max_salary = stuff_dict.get('baseSalary','').get('value','').get('maxValue','')
            self.salary_unit = stuff_dict.get('baseSalary','').get('value','').get('unitText','')
        except:
            pass
        # other
        self.job_location_type = stuff_dict.get('jobLocationType','')
        self.employment_type = stuff_dict.get('employmentType','')
        self.valid_through = stuff_dict.get('validThrough','').split('T')[0]
        self.direct_apply = stuff_dict.get('directApply','')
        self.title_again = stuff_dict.get('title','')
        self.raw_script_json = str(script_json)
        return

    def display(self):
        print('-----------------')
        print(f'URL: {self.url}')
        print(f'Scrape Date: {self.scrape_date}')
        print(f'Title: {self.title}')
        print(f'Content: {self.content[:100]}...')
        print(f'Company: {self.company}')
        print(f'Date Posted: {self.date_posted}')
        # location
        print(f'Raw Job Location: {self.raw_job_location}')
        print(f'Address Country: {self.address_country}')
        print(f'Address Locality: {self.address_locality}')
        print(f'Address Region 0: {self.address_region_0}')
        print(f'Address Region 1: {self.address_region_1}')
        print(f'Address Region 2: {self.address_region_2}')
        print(f'Postal Code: {self.postal_code}')
        # hiring organization
        print(f'Raw Hiring Organization: {self.raw_hiring_organization}')
        print(f'Hiring Organization: {self.hiring_organization}')
        # location requirements
        print(f'Raw Location Requirements: {self.raw_location_requirements}')
        print(f'Country Requirements: {self.country_requirements}')
        # salary
        print(f'Raw Base Salary: {self.raw_base_salary}')
        print(f'Salary Currency: {self.salary_currency}')
        print(f'Min Salary: {self.min_salary}')
        print(f'Max Salary: {self.max_salary}')
        print(f'Salary Unit: {self.salary_unit}')
        # other stuff
        print(f'Job Location Type: {self.job_location_type}')
        print(f'Employment Type: {self.employment_type}')
        print(f'Valid Through: {self.valid_through}')
        print(f'Direct Apply: {self.direct_apply}')
        print(f'Title Again: {self.title_again}')
        print(f'Raw Script Json: {self.raw_script_json[:100]}...')
        print('-----------------')
        return