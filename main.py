import requests 
from bs4 import BeautifulSoup
import re
import time
import sqlite3

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
    # open csv with all the links
    f = open('output.csv','r')
    
    # take link for every line
    for line in f:
        lst = line.strip().split(',')

        #skip header
        if 'https' not in lst[3]: continue

        id, country, url = lst[0], lst[1], lst[3]

        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(class_='icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title').text
        print(title)
        title = soup.find(class_=re.compile(r'title')).text
        print(title, '\n\n\n')

        company_name = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].text
        company_url = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].a['href']

        print(title,'-----',company_name,'-----',company_url)




        time.sleep(5)

        # delete line after insertion?


if __name__ == "__main__":
    # url_scraper()
    get_posts()