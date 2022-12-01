# Import modules
from bs4 import BeautifulSoup 
import requests
import database
import os

# Get Data from scraper
def get_data(tableName):
    
    database.truncateTable(tableName)

    pages = 10
    for page in range(pages):
        
        res = requests.get('https://www.kenyamoja.com/jobs?page=' + str(page))
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
                lnk = link.a.get('href').replace('&utm_source=KenyaMOJA.com', '')
                clean_links = lnk[lnk.find('https'):]
                links.append(clean_links)

            return links
    
        
        for index, jobs in enumerate(raw_jobs):
            job = []
            jobName = raw_jobs[index].getText()
            jobURL = clean_content(raw_links)[index]
            dayOfJobPost = raw_dates_posted[index].getText().strip()


            job.append(jobName)
            job.append(jobURL)
            job.append(dayOfJobPost)

            database.insertData(job, tableName)

get_data('public.availablejobs')
        