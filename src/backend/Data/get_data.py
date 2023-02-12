# Import modules
from bs4 import BeautifulSoup 
import requests
import sys
import os
path = os.getcwd()
sys.path.append(path+"/src/")
from backend import database
from dotenv import load_dotenv

load_dotenv()

# Get Data using scraper
def get_data(tableName):
    
    url = os.environ['URL1']
    dirty_string = os.environ['dirty_sting']

    print("********** STARTING DATA COLLECTION **********")

    pages = 10
    for page in range(pages):
        
        res = requests.get(str(url) + str(page))
        soup = BeautifulSoup(res.text, 'html.parser')

        # Raw Content
        raw_jobs = soup.select('.items-title')
        raw_links = soup.find_all('div', 'news-title')
        raw_dates_posted = soup.select('.items-date')

        # Clean Raw Content
        def clean_content(raw_links):	
        # return clean links
            links = []
            for link in raw_links:
                lnk = link.a.get('href').replace(str(dirty_string), '')
                clean_links = lnk[lnk.find('https'):]
                links.append(clean_links)
            return links
    
        for x in range(len(raw_jobs)):
            job = []
            jobName = raw_jobs[x].getText()
            jobURL = clean_content(raw_links)[x]
            dayOfJobPost = raw_dates_posted[x].getText().strip()

            job.append(jobName)
            job.append(jobURL)
            job.append(dayOfJobPost)

            database.insertData(job, tableName)

    print("********** DATA COLLECTION COMPLETE **********")

if __name__ == '__main__':
    
    tableName = os.environ['TABLENAME']
    get_data(tableName)
    