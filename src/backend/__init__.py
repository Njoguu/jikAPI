from flask import Flask, render_template, jsonify
from http.client import NOT_FOUND, INTERNAL_SERVER_ERROR
import os
import sys
path = os.getcwd()
sys.path.append(path+"/src/")
from flasgger import Swagger
from backend.config.swagger import swagger_config,template
from backend.auth import auth
from backend.postings import postings
from backend.newsletter import newsletter
from Data.get_data import get_data as scraper1
from Data.get_data2 import get_data as scraper2
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import datetime
from backend.config.caching import cache

load_dotenv()

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'
   
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    

    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = 'redis'
    app.config['CACHE_REDIS_PORT'] = 7505

    # Schedule jobs to be run
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(scraper1, "interval", hours=1)
    scheduler.add_job(scraper2, "interval", hours=1.5)
    scheduler.start()

    # Initialize the cache
    cache.init_app(app)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ["SECRET_KEY"],
            SQLALCHEMY_TRACK_MODIFICATIONS=False, 
            JWT_SECRET_KEY=os.environ["JWT_SECRET_KEY"],

            SWAGGER = {
                "title" : "jikAPI",
                "uiversion" : 3,
            }
        )        

    else:
        app.config.from_mapping(test_config)

    # Register blueprints here
    app.register_blueprint(blueprint=auth)
    app.register_blueprint(blueprint=postings)
    app.register_blueprint(blueprint=newsletter)

    recaptcha_API_key = os.environ['RECAPTCHA_API_KEY']

    JWTManager(app)

    Swagger(app, config=swagger_config, template=template)

    # Route to homepage
    @app.route('/')
    @cache.cached(timeout=300)
    def homepage():
        message = "Streamline your job search with this Job Search API. Check it out! #jobs #API"
        url = "https://jikapi.herokuapp.com"

        current_year = datetime.date.today().year

        tweet_link = "https://twitter.com/intent/tweet?text=" + message + "&url=" + url
        linkedin_link = "https://www.linkedin.com/sharing/share-offsite/?url=" + url
        facebook_link = "https://www.facebook.com/sharer/sharer.php?u=" + url
        
        return render_template('index.html', tweet_link=tweet_link, linkedin_link=linkedin_link, facebook_link=facebook_link, current_year=current_year, site_key=recaptcha_API_key)

    @app.errorhandler(NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), NOT_FOUND

    @app.errorhandler(INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), INTERNAL_SERVER_ERROR

    return app
    
