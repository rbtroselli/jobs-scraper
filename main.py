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
with open('output.csv','w') as f:

    # iterate for every country in dictionary
    for key in dict:
        url = f'https://{dict[key]}indeed.com/jobs?q="data%20engineer"&start='
        
        j=1

        # iterate for every page (1-66)
        for i in range(0,2):
            url2 = url + str(i*10)
            print(url2)

            # get the page, parse with beautifulsoup
            page = requests.get(url2)
            soup = BeautifulSoup(page.content,'html.parser')   

            # iterate for every post in page
            # find every a tag with 'result' as part of the class name
            for element in soup.find_all('a', {'class':re.compile(r'result')}):
                # write the country dict key, the url, the job id
                f.write(f"{element['id']},https://{dict[key]}indeed.com{element['href']},{key},{j}\n")
                j+=1
            time.sleep(3)