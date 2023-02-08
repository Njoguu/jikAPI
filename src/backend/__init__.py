from flask import Flask, render_template
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

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'
   
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False, 
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),

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
        
        return render_template('index.html', tweet_link=tweet_link, linkedin_link=linkedin_link, facebook_link=facebook_link)

    return app
    