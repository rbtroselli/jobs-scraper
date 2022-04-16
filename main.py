import requests 
from bs4 import BeautifulSoup
import re
import time
import webbrowser

# url = 'https://www.indeed.com/jobs?q=data%20engineer'
# url = 'https://indeed.com/jobs?q=data%20engineer&start='
i = 0

# dictionary with country tag and corresponding url piece
dict = {'us':'', 'it':'it.', 'uk':'uk.'}

# open file to write results
# avoid with for indentation
f = open('output.csv','w')
f.write("id,country,n,url\n")

# iterate for every country in dictionary
for key in dict:
    url = f'https://{dict[key]}indeed.com/jobs?q="data%20engineer"&start='
    
    # just checking number of posts per page in CSV
    j=1

    # iterate for every page (1-66)
    for i in range(0,2):
        url2 = url + str(i*10)
        print(url2)

        # get the page, parse with beautifulsoup
        page = requests.get(url2)
        soup = BeautifulSoup(page.content,'html.parser') 

        #printing response
        print(page)

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