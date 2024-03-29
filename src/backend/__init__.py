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
# from backend.Data.get_data import get_data as scraper1
# from backend.Data.get_data2 import get_data as scraper2
from flask_jwt_extended import JWTManager
# from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'
   
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    


    # app.config['CACHE_TYPE'] = 'redis'
    # app.config['CACHE_REDIS_HOST'] = 'redis'
    # app.config['CACHE_REDIS_PORT'] = 7505

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

    # Initialize the rate limiter
    limiter = Limiter(
                app=app,
                key_func=get_remote_address,
                enabled=True,
                default_limits=["40 per day", "5 per minute"],
                storage_uri=os.environ["REDIS_URL"] + "/1" + "?ssl_cert_reqs=none",  
                storage_options={"socket_connect_timeout": 30},
                strategy="fixed-window"
            )

    limiter.limit("5 per minute", error_message="5 requests per minute")(postings)

    recaptcha_API_key = os.environ['RECAPTCHA_API_KEY']

    JWTManager(app)

    Swagger(app, config=swagger_config, template=template)

    # Route to homepage
    @app.route('/')
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
    
