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

def get_data(tableName):

	print("********** STARTING DATA COLLECTION **********")

	pages = 5
	for page in range(pages):

		# Send a GET request to the URL
		url = os.environ['url']
		url2 = os.environ['URL2']
		res = requests.get(str(url2) + str(page))

		# Parse the HTML content of the page
		soup = BeautifulSoup(res.text, 'html.parser')

		# Find the job listings
		job_listings = soup.find_all('li', 'mag-b')
		dates_posted = soup.find_all('li', id='job-date')

		for x in range(len(job_listings)):
			job = []
			jobName = job_listings[x].getText().strip()
			dayOfJobPost = dates_posted[x].getText()
			jobURL = str(url)+job_listings[x].a.get('href')

			job.append(jobName)
			job.append(jobURL)
			job.append(dayOfJobPost)

			database.insertData(job, tableName)

	print("********** DATA COLLECTION COMPLETE **********")

if __name__ == '__main__':
    
    tableName = os.environ['TABLENAME']
    get_data(tableName)
