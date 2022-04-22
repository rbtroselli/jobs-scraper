import requests 
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date
import traceback
import random
from freeproxy import FreeProxyCollection

def url_scraper(path=''):
    # dictionary with country tag and corresponding url piece
    dict = {'us':'', 'it':'it.', 'uk':'uk.', 'es':'es.', 'fr':'fr.', 'de':'de.', 'at':'at.', 'be':'be.', 'ca':'ca.', 'fi':'fi.', 'dk':'dk.', 'cz':'cz.', 'gr':'gr.', 'hu':'hu.',
                     'ie':'ie.', 'lu':'lu.', 'nl':'nl.', 'no':'no.', 'pl':'pl.', 'pt':'pt.', 'ro':'ro.', 'se':'se.', 'ch':'ch.', 'ua':'ua.', 
                     'ar':'ar.', 'au':'au.', 'bh':'bh.', 'br':'br.', 'cl':'cl.', 'ch':'ch.', 'co':'co.', 'cr':'cr.', 'ec':'ec.', 'eg':'eg.', 'hk':'hk.', 'in':'in.', 'id':'id.',
                     'il':'il.', 'jp':'jp.', 'kw':'kw.', 'mx':'mx.', 'ma':'ma.', 'nz':'nz.', 'ng':'ng.', 'om':'om.', 'pk':'pk.', 'pa':'pa.', 'pe':'pe.', 'ph':'ph.', 'qa':'qa.',
                     'sa':'sa.', 'sg':'sg.', 'za':'za.', 'kr':'kr.', 'tw':'tw.', 'th':'th.', 'tr':'tr.', 'ae':'ae.', 'uy':'uy.', 've':'ve.', 'vn':'vn.', 'my':'malaysia.'}
    urls_file = path + 'data/urls.csv'
    f = open(urls_file,'w')
    f.write("number,job_id,job_role,country,job_url\n")
    
    # keep same sessione
    fpc = FreeProxyCollection()
    proxy = fpc.get_proxy()
    s = requests.Session()
    s.proxies = {'https':proxy}

    for job in ['data+engineer','data+scientist','data+analyst']:

        # iterate for every country in dictionary
        for key in dict:
 

            url = f'https://{dict[key]}indeed.com/jobs?q="{job}"&sort=date&filter=0&start='
            job_role_acronym = ''.join(word[0] for word in job.split('+'))
            # only last day &fromage=1
            
            # just checking number of posts per page in CSV
            j=1

            # id list to append ids and check duplicates to break loop
            id_list = []
            
            # iterate for every page (1-66)
            for i in range(0,1000):
                
                # try to get the page until no error, than break
                while True:
                    try:
                        # combine the url with page number (multiplied), get the page, parse with bs
                        url2 = url + str(i*10)
                        page = s.get(url2, timeout=6)
                        soup = BeautifulSoup(page.content,'html.parser')
                        break
                    except Exception as e:
                        print('Error 1')
                        proxy = fpc.get_proxy()
                        s.proxies = {'https':'https://'+proxy}
                        print(e)
                
                # if page contains captcha, change proxy and get again
                while 'captcha' in soup.text.lower(): 
                    while True:
                        try:
                            print('captcha')
                            proxy = fpc.get_proxy()
                            s.proxies = {'https':'https://'+proxy}
                            page = s.get(url2, timeout=6)
                            soup = BeautifulSoup(page.content,'html.parser')
                            break
                        except Exception as e:
                            print(e)
                    
                # break condition, if url is already present (Indeed last page is looping)
                if soup.find('a', {'id':re.compile(r'job_')})['id'][4:] in id_list: break

                # iterate for every post in page
                # find every a tag with 'job_' as part of the id name, and get job_id from there
                for element in soup.find_all('a', {'id':re.compile(r'job_')}):
                    job_id = element['id'][4:]
                    f.write(f"{j},{job_id},{job_role_acronym},{key},https://www.indeed.com/viewjob?jk={job_id}\n")
                    id_list.append(job_id)
                    print(j,key,job_role_acronym,job_id)
                    j+=1
                f.flush()
                time.sleep(random.uniform(3,5))
    
    f.close()
    return


def post_scraper(path=''):

    urls_file = path + 'data/urls.csv'
    staging_file = path + 'data/staging.csv'

    # create a df from the output from previous step, with urls of job posts
    # open a file to write scraped data
    df = pd.read_csv(urls_file)
    f = open(staging_file,'w')
    f.write(f'"job_id","job_role","post_title","post_url","company_name","company_url","country","location","job_type","salary","scrape_date","posted","info_remote","description"\n')

    fpc = FreeProxyCollection()
    proxy = fpc.get_proxy()
    # s = requests.Session()
    proxies = {'https':proxy}
    
    # iterate df rows
    for index,row in df.iterrows():
        job_id, job_role, country, post_url = row['job_id'], row['job_role'], row['country'], row['job_url']
        
        # try 10 times, on fail change proxy
        for attempt in range(10):
            try:
                page = requests.get(post_url, proxies=proxies)
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

                print(f'{job_id}\n{job_role}\n{post_title}\n{post_url}\n{company_name}\n{company_url}\n{country}\n{location}\n{job_type}\n{salary}\n{scrape_date}\n{posted}\n{info_remote}\n')
                line = f'"{job_id}","{job_role}","{post_title}","{post_url}","{company_name}","{company_url}","{country}",'\
                    f'"{location}","{job_type}","{salary}","{scrape_date}","{posted}","{info_remote}","{description}"\n'
                f.write(line)

            # change proxy and attempt again
            except Exception as e:
                print(attempt,post_url,'\n',e)
                proxy = fpc.get_proxy()
                proxies = {'https':proxy}

        
        f.flush()
        time.sleep(random.uniform(3,5))
    
    f.close()
    return


if __name__ == "__main__":
    url_scraper()
    # post_scraper()