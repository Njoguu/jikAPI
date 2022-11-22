from flask import Flask, render_template
import os

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'
    
    app = Flask(__name__, instance_relative_config=True, template_folder=template_dir, static_folder=static_dir)    



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

    @app.route('/api/v1/')
    def versions():
        return render_template('versions.html')

    @app.route('/api/v1/jobs')
    def available_jobs():
        pass

    return app