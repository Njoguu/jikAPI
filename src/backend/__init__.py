from flask import Flask, render_template, request
import os
import src.backend.database as dbcons
from src.backend.get_data import get_data as scraper
from apscheduler.schedulers.background import BackgroundScheduler

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(id='Scheduled Task', func=scraper, trigger='cron', day_of_week='mon-sun', hour='*')
    scheduler.start()
    
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    
    keyword = ""


    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    # @app.route('/', methods=["GET", "POST"])
    # def homepage():
    #     # if user submits the form
    #     if request.method == "POST":
    #         email = request.form.get('email')

    #         dbcons.subscribe_user(email=email, user_group_email="", api_key="")


    #     return render_template('index.html')

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

    return app
    