import requests 
from bs4 import BeautifulSoup
import re
import time

# url = 'https://www.indeed.com/jobs?q=data%20engineer'
# url = 'https://indeed.com/jobs?q=data%20engineer&start='
i = 0

# dictionary with country tag and corresponding url piece
dict = {'us':'', 'it':'it.', 'uk':'uk.'}

# open file to write results
# avoid with for indentation
f = open('output.csv','w')
o = open('output.txt','w')

# iterate for every country in dictionary
for key in dict:
    url = f'https://{dict[key]}indeed.com/jobs?q="data%20engineer"&start='
    
    # just checking number of posts per page in CSV
    j=1

    # iterate for every page (1-66)
    for i in range(0,3):
        url2 = url + str(i*10)
        print(url2)

        # get the page, parse with beautifulsoup
        page = requests.get(url2)
        soup = BeautifulSoup(page.content,'html.parser') 

        #printing response
        print(page)

        # check why pages jump sometimes
        o.write(soup.text)
        o.write('\n\n\n\n\n\n\n\n\n\n\n\n######################\n\n\n\n\n\n\n\n\n\n\n')  

        # iterate for every post in page
        # find every a tag with 'result' as part of the class name
        for element in soup.find_all('a', {'class':re.compile(r'result')}):
            print(j)
            time.sleep(0.5)
            # write the country dict key, the url, the job id
            f.write(f"{element['id']},https://{dict[key]}indeed.com/viewjob{element['href'][7:]},{key},{j}\n")
            j+=1
        time.sleep(5)

f.close()
o.close()