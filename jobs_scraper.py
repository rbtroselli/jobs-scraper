import requests 
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date
import traceback

def url_scraper(path=''):
    # dictionary with country tag and corresponding url piece
    dict = {'us':'', 'it':'it.', 'uk':'uk.'}

    urls_file = path + 'data/urls.csv'

    # open file to write results
    # avoid with for indentation
    f = open(urls_file,'w')
    f.write("job_id,country,number,job_url\n")

    # iterate for every country in dictionary
    for key in dict:
        url = f'https://{dict[key]}indeed.com/jobs?q="data%20engineer"&start='
        
        # just checking number of posts per page in CSV
        j=1

        # iterate for every page (1-66)
        for i in range(0,1):

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
    return


def post_scraper(path=''):

    urls_file = path + 'data/urls.csv'
    staging_file = path + 'data/staging.csv'
    errors_file = path + 'data/errors.txt'

    # create a df from the output from previous step, with urls of job posts
    # open a file to write scraped data
    df = pd.read_csv(urls_file)
    f = open(staging_file,'w')
    f.write(f'"job_id","post_title","post_url","company_name","company_url","country","location","job_type","salary","scrape_date","posted","info_remote","description"\n')
    err = open(errors_file,'w')
    
    # iterate df rows
    for index,row in df.iterrows():
        job_id, country, post_url = row['job_id'], row['country'], row['job_url']
        
        try:
            page = requests.get(post_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # scrape all the needed data. location from the title, it's consistent between languages
            post_title = soup.find(class_='jobsearch-JobInfoHeader-title-container').text
            company_name = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].text
            try: company_url = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].a['href']
            except: company_url = ''
            try: job_type = soup.find(id='salaryInfoAndJobType').find(class_='jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs').text.strip(' -')
            except: job_type = ''
            try: salary = soup.find(id='salaryInfoAndJobType').find(class_='icl-u-xs-mr--xs attribute_snippet').text
            except: salary = ''
            posted = soup.find_all(class_='jobsearch-HiringInsights-entry--text')[-1].text
            location = soup.find('title').text.split('-')[-2].strip()
            scrape_date = date.today() ## ATTENZIONE! Substitute with Airflow function
            info_remote = soup.find(class_='jobsearch-CompanyInfoContainer').get_text(separator=' - ') # this may contain the REMOTE keyword
            description = soup.find(class_='jobsearch-jobDescriptionText').text.replace('"','\'') # replace to avoid messing CSV up

            print(f'{job_id}\n{post_title}\n{post_url}\n{company_name}\n{company_url}\n{country}\n{location}\n{job_type}\n{salary}\n{scrape_date}\n{posted}\n{info_remote}\n')

            line = f'"{job_id}","{post_title}","{post_url}","{company_name}","{company_url}","{country}",'\
                f'"{location}","{job_type}","{salary}","{scrape_date}","{posted}","{info_remote}","{description}"\n'
            f.write(line)

        except Exception as e:
            print('ERROR', e)
            print(post_url)
            print(traceback.format_exc())
            err.write(f'{post_url}\n{traceback.format_exc()}\n\n\n')
        time.sleep(5)

        # delete line after insertion?
    
    f.close()
    err.close()
    return


if __name__ == "__main__":
    url_scraper()
    post_scraper()