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
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'
   
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False, 
            JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),

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

    recaptcha_API_key = os.getenv('RECAPTCHA_API_KEY')

    JWTManager(app)

    Swagger(app, config=swagger_config, template=template)

    # Route to homepage
    @app.route('/')
    def homepage():
        message = "Streamline your job search with this Job Search API. Check it out! #jobs #API"
        url = "https://jikapi.herokuapp.com"

        tweet_link = "https://twitter.com/intent/tweet?text=" + message + "&url=" + url
        linkedin_link = "https://www.linkedin.com/sharing/share-offsite/?url=" + url
        facebook_link = "https://www.facebook.com/sharer/sharer.php?u=" + url
        
        return render_template('index.html', tweet_link=tweet_link, linkedin_link=linkedin_link, facebook_link=facebook_link, site_key=recaptcha_API_key)

    @app.errorhandler(NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), NOT_FOUND

    @app.errorhandler(INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), INTERNAL_SERVER_ERROR

    return app
    