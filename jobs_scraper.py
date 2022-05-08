import requests 
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from datetime import date
import traceback
import random
import langdetect

def url_scraper(path=''):
    # dictionary with country tag and corresponding url piece
    dict = {'us':'', 'it':'it.', 'uk':'uk.', 'es':'es.', 'fr':'fr.', 'de':'de.', 'at':'at.', 'be':'be.', 'ca':'ca.', 'fi':'fi.', 'dk':'dk.', 'cz':'cz.', 'gr':'gr.', 'hu':'hu.',
                     'ie':'ie.', 'lu':'lu.', 'nl':'nl.', 'no':'no.', 'pl':'pl.', 'pt':'pt.', 'ro':'ro.', 'se':'se.', 'ch':'ch.', 'ua':'ua.', 
                     'ar':'ar.', 'au':'au.', 'bh':'bh.', 'br':'br.', 'cl':'cl.', 'ch':'ch.', 'co':'co.', 'cr':'cr.', 'ec':'ec.', 'eg':'eg.', 'hk':'hk.', 'in':'in.', 'id':'id.',
                     'il':'il.', 'jp':'jp.', 'kw':'kw.', 'mx':'mx.', 'ma':'ma.', 'nz':'nz.', 'ng':'ng.', 'om':'om.', 'pk':'pk.', 'pa':'pa.', 'pe':'pe.', 'ph':'ph.', 'qa':'qa.',
                     'sa':'sa.', 'sg':'sg.', 'za':'za.', 'kr':'kr.', 'tw':'tw.', 'th':'th.', 'tr':'tr.', 'ae':'ae.', 'uy':'uy.', 've':'ve.', 'vn':'vn.', 'my':'malaysia.'}
    urls_file = path + 'data/urls.csv'
    f = open(urls_file,'w')
    f.write("number,job_id,job_role,job_role_ext,country,job_url\n")

    urls_error_file = path + 'data/urls_error.txt'
    err = open(urls_error_file, 'w')

    for job in ['data%20engineer','data%20scientist']:
        job_role = ''.join(word[0] for word in job.split('%20'))
        job_role_ext = ' '.join(word for word in job.split('%20'))

        # iterate for every country in dictionary
        for key in dict:
            # only last day &fromage=1
            url = f'https://{dict[key]}indeed.com/jobs?q="{job}"&sort=date&fromage=1&filter=0&start='
            
            # just checking number of posts per page in CSV
            j=1

            # id list to append ids and check duplicates to break loop
            id_list = []

            finish, captcha, error_3 = False, False, False

            # iterate for every page (1-66)
            for i in range(0,1000):
                if finish == True: break
                if captcha == True: break
                if error_3 == True: break

                # three attempts
                for attempt in range(3):
                    
                    try:
                        # combine the url with page number (multiplied), get the page, parse with bs
                        url2 = url + str(i*10)
                        page = requests.get(url2)
                        soup = BeautifulSoup(page.content,'html.parser')
                        print(url2+'\n')

                        # break for loop, if captcha
                        if 'captcha' in soup.text.lower(): 
                            print(f'@@@@@@@@ CAPTCHA @@@@@@@@\n{url2}\n')
                            err.write(f'@@@@@@@@ CAPTCHA @@@@@@@@\n{url2}\n\n\n')
                            captcha = True
                            break
                        
                        current_id_list = []
                        for element in soup.find_all('a', {'id':re.compile(r'job_')}):
                            current_id_list.append(element['id'][4:])
                        # break for loop, if all jobs in the page are already present (Indeed loop)
                        if set(current_id_list).issubset(set(id_list)): 
                            print('FINISH')
                            time.sleep(random.uniform(5,10))
                            finish = True
                            break

                        # iterate for every post in page
                        # find every a tag with 'job_' as part of the id name
                        for element in soup.find_all('a', {'id':re.compile(r'job_')}):
                            # take job id, skip if job_id is already present. If not add to iteration list
                            job_id = element['id'][4:]
                            if job_id in id_list: 
                                continue 
                            id_list.append(job_id)

                            # take post block, skip if doesn't contain the role
                            if job_role_ext not in element.text.lower():
                                print(f'{url2}\n{element.text}\n{job_role_ext}\nOUT!!!\n')
                                err.write(f'{url2}\n{element.text}\n{job_role_ext}\nOUT!!!\n\n\n')
                                continue

                            # write to file all needed information 
                            print(f"{j},{job_id},{job_role},{job_role_ext},{key},https://www.indeed.com/viewjob?jk={job_id}")
                            f.write(f"{j},{job_id},{job_role},{job_role_ext},{key},https://www.indeed.com/viewjob?jk={job_id}\n")
                            j+=1
                        f.flush()
                        time.sleep(random.uniform(5,10))
                        # break from attempts if above for is successfull
                        break

                    # if there's any error raised, try a couple more times
                    except Exception as e:
                        print(f'@@@@@@@@ ERROR @@@@@@@@\n{attempt}\n{url2}\n{e}\n')
                        print(traceback.format_exc())
                        err.write(f'@@@@@@@@ ERROR @@@@@@@@\n{attempt}\n{url2}\n{e}\n')
                        err.write(traceback.format_exc())
                        err.write('\n\n\n')
                        err.flush()
                        if attempt == 2: error_3 = True # avoid infinite loops
    
    f.close()
    err.close()
    return


def post_scraper(path=''):

    urls_file = path + 'data/urls.csv'
    staging_file = path + 'data/staging.csv'

    # create a df from the output from previous step, with urls of job posts
    # open a file to write scraped data
    df = pd.read_csv(urls_file)
    f = open(staging_file,'w')
    f.write(f'"job_id","job_role","job_role_ext","post_title","post_url","company_name","company_url","country","location","job_type","salary","scrape_date","posted","info_remote","post_language","description"\n')
    
    posts_error_file = path + 'data/posts_error.txt'
    err = open(posts_error_file, 'w')

    # iterate df rows
    for index,row in df.iterrows():
        job_id, job_role, job_role_ext, country, post_url = row['job_id'], row['job_role'], row['job_role_ext'], row['country'], row['job_url']
        
        for attempt in range(3):
            try:
                page = requests.get(post_url)
                soup = BeautifulSoup(page.content, 'html.parser')

                # break for loop, if captcha
                if 'captcha' in soup.text.lower(): 
                    print(f'@@@@@@@@ CAPTCHA @@@@@@@@\n{post_url}\n')
                    err.write(f'@@@@@@@@ CAPTCHA @@@@@@@@\n{post_url}\n\n\n')
                    break

                # scrape all the needed data. location from the title, it's consistent between languages
                post_title = soup.find(class_='jobsearch-JobInfoHeader-title-container').text.replace('"','\'')

                # catch intruders, another check for what passed previous one
                if job_role_ext not in post_title.lower(): 
                    print(f'{post_url}\n{post_title}\n{job_role_ext}\nOUT!!!\n')
                    err.write(f'{post_url}\n{post_title}\n{job_role_ext}\nOUT!!!\n\n\n')
                    break 
                
                company_name = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].text.replace('"','\'')
                try: company_url = soup.find_all(class_='icl-u-lg-mr--sm icl-u-xs-mr--xs')[1].a['href']
                except: company_url = ''
                try: job_type = soup.find(id='salaryInfoAndJobType').find(class_='jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs').text.strip(' -')
                except: job_type = ''
                try: salary = soup.find(id='salaryInfoAndJobType').find(class_='icl-u-xs-mr--xs attribute_snippet').text
                except: salary = ''
                posted = soup.find_all(class_='jobsearch-HiringInsights-entry--text')[-1].text
                location = soup.find('title').text.split('-')[-2].strip()
                scrape_date = date.today() 
                info_remote = soup.find(class_='jobsearch-CompanyInfoContainer').get_text(separator=' - ').text.replace('"','\'') # this may contain the REMOTE keyword
                description = soup.find(class_='jobsearch-jobDescriptionText').text.replace('"','\'') # replace to avoid messing CSV up
                post_language = langdetect.detect(description) # detect post language (this info is not exposed in web page)

                print(f'{job_id}\n{job_role}\n{job_role_ext}\n{post_title}\n{post_url}\n{company_name}\n{company_url}\n{country}'\
                    f'\n{location}\n{job_type}\n{salary}\n{scrape_date}\n{posted}\n{info_remote}\n{post_language}\n--------------------------------')
                line = f'"{job_id}","{job_role}","{job_role_ext}","{post_title}","{post_url}","{company_name}","{company_url}","{country}",'\
                    f'"{location}","{job_type}","{salary}","{scrape_date}","{posted}","{info_remote}","{post_language}","{description}"\n'
                f.write(line)
                # break from attempt if all of the aobve is successfull
                break

            except Exception as e:
                print(f'@@@@@@@@ ERROR @@@@@@@@\n{attempt}\n{post_url}\n{e}\n')
                print(traceback.format_exc())
                err.write(f'@@@@@@@@ ERROR @@@@@@@@\n{attempt}\n{post_url}\n{e}\n')
                err.write(traceback.format_exc())
                err.write('\n\n\n')
                err.flush()
                
        f.flush()
        time.sleep(random.uniform(5,10))
    
    f.close()
    err.close()
    return


if __name__ == "__main__":
    url_scraper()
    post_scraper()