import requests 
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date
import traceback

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
    f.write(f'"job_id","title","url","company_name","company_page","country","location","job_type","salary","scrape_date","posted","info_remote","description"\n')
    err = open('errors.txt','w')
    
    # iterate df rows
    for index,row in df.iterrows():
        job_id, country, url = row['job_id'], row['country'], row['job_url']
        
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # scrape all the needed data. location from the title, it's consistent between languages
            title = soup.find(class_='jobsearch-JobInfoHeader-title-container').text
            company_name = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].text
            try: company_page = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].a['href']
            except: company_page = ''
            try: job_type = soup.find(id='salaryInfoAndJobType').find(class_='jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs').text.strip(' -')
            except: job_type = ''
            try: salary = soup.find(id='salaryInfoAndJobType').find(class_='icl-u-xs-mr--xs attribute_snippet').text
            except: salary = ''
            posted = soup.find_all(class_='jobsearch-HiringInsights-entry--text')[-1].text
            location = soup.find('title').text.split('-')[-2].strip()
            scrape_date = date.today() ## ATTENZIONE! Substitute with Airflow function
            info_remote = soup.find(class_='jobsearch-CompanyInfoContainer').get_text(separator=' - ') # this may contain the REMOTE keyword
            description = soup.find(class_='jobsearch-jobDescriptionText').text.replace('"','\'') # replace to avoid messing CSV up

            print(f'{job_id}\n{title}\n{url}\n{company_name}\n{company_page}\n{country}\n{location}\n{job_type}\n{salary}\n{scrape_date}\n{posted}\n{info_remote}\n')

            line = f'"{job_id}","{title}","{url}","{company_name}","{company_page}","{country}",'\
                f'"{location}","{job_type}","{salary}","{scrape_date}","{posted}","{info_remote}","{description}"\n'
            f.write(line)

        except Exception as e:
            print('ERROR', e)
            print(url)
            print(traceback.format_exc())
            err.write(f'{url}\n{traceback.format_exc()}\n\n\n')
        time.sleep(5)

        # delete line after insertion?
    
    f.close()
    err.close()


if __name__ == "__main__":
    # url_scraper()
    get_posts()

    df = pd.read_csv('staging.csv')
    print(df)