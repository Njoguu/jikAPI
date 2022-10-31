import requests
from bs4 import BeautifulSoup
import json
import time

# write tests for response
for page in range(1,4):

	res = requests.get('https://www.kenyamoja.com/jobs?page=' + str(page))
	soup = BeautifulSoup(res.text, 'html.parser')

	# Content
	raw_jobs = soup.select('.items-title')
	raw_links = soup.find_all('div', 'news-title')
	raw_dates_posted = soup.select('.items-date')

	# return clean content
	def clean_content(raw_links):
		# return clean links
		links = []
		for link in raw_links:
			lnk = link.a.get('href').replace('&utm_source=KenyaMOJA.com', '')
			clean_links = lnk[lnk.find('https'):]
			links.append(clean_links)
		
		return links

	def sort_jobs(info):
		return sorted(info, key= lambda k:k['Title'])


	def create_info(raw_jobs, links, raw_dates_posted):
		info = []
		for index, job in enumerate(raw_jobs):
			job_title = raw_jobs[index].getText()
			job_link = links[index]
			date_posted = raw_dates_posted[index].getText().strip()
			info.append(
				{
				'Title' : job_title,
				'Application Link' : job_link,
				'Date Posted' : date_posted
				}
				)
		all_jobs = sort_jobs(info)
		json_object = json.dumps(all_jobs, indent=4)
		return json_object

	print(create_info(raw_jobs,clean_content(raw_links),raw_dates_posted))
