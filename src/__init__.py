from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import os
from src.database import db
# import json
# import time

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)    

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    # @app.route('/')
    # def homepage():
    #     return render_template('index.html')

    # @app.route('/api/v1/')
    # def versions():
    #     return render_template('versions.html')

    # @app.route('/api/v1/jobs')
    # def available_jobs():
    #     res = requests.get('https://www.kenyamoja.com/jobs?page=')
    #     soup = BeautifulSoup(res.text, 'html.parser')

    #     # Content
    #     raw_jobs = soup.select('.items-title')
    #     raw_links = soup.find_all('div', 'news-title')
    #     raw_dates_posted = soup.select('.items-date')

    #     # return clean content
    #     def clean_content(raw_links):
    #         # return clean links
    #         links = []
    #         for link in raw_links:
    #             lnk = link.a.get('href').replace('&utm_source=KenyaMOJA.com', '')
    #             clean_links = lnk[lnk.find('https'):]
    #             links.append(clean_links)
            
    #         return links

    #     def sort_jobs(info):
    #         return sorted(info, key= lambda k:k['Title'])


    #     def create_info(raw_jobs, links, raw_dates_posted):
    #         info = []
    #         for index, job in enumerate(raw_jobs):
    #             job_title = raw_jobs[index].getText()
    #             job_link = links[index]
    #             date_posted = raw_dates_posted[index].getText().strip()
    #             info.append(
    #                 {
    #                 'Title' : job_title,
    #                 'Application Link' : job_link,
    #                 'Date Posted' : date_posted
    #                 }
    #                 )
    #         all_jobs = sort_jobs(info)
    #         return jsonify(all_jobs)

    #     return create_info(raw_jobs,clean_content(raw_links),raw_dates_posted)


    db.app = app
    db.init_app(app)
        
    # @app.route('/api/v1/jobs/<int:job_id>')
    # def specific_available_jobs(job_id):
    #     return render_template('specific_job', job_id=job_id)
    return app