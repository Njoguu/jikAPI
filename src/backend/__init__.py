from flask import Flask, render_template, request, jsonify
import os
import src.backend.database as dbcons
from src.backend.get_data import get_data as scraper
from apscheduler.schedulers.background import BackgroundScheduler
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(id='Scheduled Task', func=scraper, trigger='cron', day_of_week='mon-sun', hour='*')
    scheduler.start()   

    mailchimp = Client()
    mailchimp.set_config({
        'api_key': os.environ.get('MAILCHIMP_API_KEY'),
        'server': os.environ.get('MAILCHIMP_REGION'),
    })
    
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    
    keyword = ""
    specified_date = "" 


    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def homepage():
        
        return render_template('index.html')

    @app.route('/api/v2/jobs', methods=['GET'])
    def available_jobs():
        return dbcons.getData(tableName=os.environ.get('TABLENAME'))
        
    # Using Query parameters
    @app.route('/api/v2/jobs/keyword')
    def qspecific_jobs():
        
        global keyword
        keyword = request.args.get('jobname', type=str)

        return dbcons.get_specific_job(tableName=os.environ.get('TABLENAME'))
        
    
    @app.route('/api/v2/jobs/keyword', methods = ['POST'])
    def specific_jobs():
        reqJSON = request.get_json()

        global keyword
        keyword = reqJSON['keyword']

        return dbcons.get_specific_job(tableName=os.environ.get('TABLENAME'))

    @app.route('/api/v2/jobs', methods=['POST'])
    def date_specified():
        reqJSON = request.get_json()

        global specified_date
        specified_date = reqJSON['specified_date']

        return dbcons.get_job_of_specific_date(tableName=os.environ.get('TABLENAME'))

    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        # add the email address to your mailing list here
        if request.method == 'POST':
            try:
                email = request.form['email']
                member_info = {
                    'email_address': email,
                    'status': 'subscribed',
                }
                response = mailchimp.lists.add_list_member(
                    os.environ.get('MAILCHIMP_MARKETING_AUDIENCE_ID'),
                    member_info,
                )
                return 'Thanks for subscribing!'

            except ApiClientError as error:
                return 'Subscriber Error!'

        return 'Thanks for subscribing!'

    # TODO --> SEND PING TO TESTS
    @app.route('/ping')
    def mailchimp_ping_view():
        response = mailchimp.ping.get()
        return jsonify(response)


    return app
    