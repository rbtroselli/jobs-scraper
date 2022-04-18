import requests 
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date

def url_scraper():
    # dictionary with country tag and corresponding url piece
    dict = {'us':'', 'it':'it.', 'uk':'uk.'}

    # open file to write results
    # avoid with for indentation
    f = open('output.csv','w')
    f.write("job_id,country,number,job_url\n")

    # iterate for every country in dictionary
    for key in dict:
        url = f'https://{dict[key]}indeed.com/jobs?q="data%20engineer"&start='
        
        # just checking number of posts per page in CSV
        j=1

        # iterate for every page (1-66)
        for i in range(0,2):

            # combine the url, get the page, parse with bs
            url2 = url + str(i*10)
            page = requests.get(url2)
            soup = BeautifulSoup(page.content,'html.parser') 

            # iterate for every post in page
            # find every a tag with 'job_' as part of the id name
            for element in soup.find_all('a', {'id':re.compile(r'job_')}):
                print(j)
                time.sleep(0.3)
                # take job id
                id = element['id'][4:]
                # job id is sufficient to retrieve the job page
                # write if, country, n, link
                f.write(f"{id},{key},{j},https://www.indeed.com/viewjob?jk={id}\n")
                j+=1
            time.sleep(3)
    f.close()


def get_posts():
    # create a df from the output from previous step, with urls of job posts
    # open a file to write scraped data
    df = pd.read_csv('output.csv')
    f = open('staging.csv','w')
    # f.write(f'colonne')
    
    err = open('errors.txt','w')
    
    # iterate df rows
    for index,row in df.iterrows():
        id, country, url = row['job_id'], row['country'], row['job_url']
        
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            print(url)
            
            # scrape all the needed data. location from the title, it's consistent between languages
            title = soup.find(class_=re.compile(r'title')).text
            company_name = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].text
            company_url = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].a['href']
            
            # try: type_salary_info = soup.find(id='salaryInfoAndJobType')
            # except: type_salary_info = 'No info'
            
            type_salary_info = soup.find(id='salaryInfoAndJobType')
            try: job_type = type_salary_info.find_all('span')[-1].text
            except: job_type = 'No info'
            try: salary = type_salary_info.find_all('span')[-2].text
            except: salary = 'No info'

            location = soup.find('title').text.split('-')[-2].strip()
            scrape_date = date.today() ## ATTENZIONE! Substitute with Airflow function

            f.write(f'"{title}","{company_name}","{company_url}"\n')

            print(f'{id}\n{title}\n{url}\n{company_name}\n{company_url}\n{country}\n{location}\n{type_salary_info}\n{job_type}\n{salary}\n{scrape_date}\n')
        
        except Exception as e:
            err.write(f'{url}\n{e}\n\n\n')
            



        time.sleep(5)

        # delete line after insertion?
    
    f.close()
    err.close()


if __name__ == "__main__":
    # url_scraper()
    get_posts()