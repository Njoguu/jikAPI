from flask import Flask, render_template, request
import os
import src.backend.database as dbcons

def create_app(test_config=None):

    template_dir = os.getcwd() + '/src/frontend/templates'
    static_dir = os.getcwd() + '/src/frontend/static'
    
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

    @app.route('/')
    def homepage():
        return render_template('index.html')

    @app.route('/api/v2/jobs', methods=['GET'])
    def available_jobs():
        return dbcons.getData(tableName=os.environ.get('TABLENAME'))
        
    # Using Query parameters
    # @app.route('/api/v2/jobs/keyword', methods = ['POST'])
    # def specific_jobs():
    #     jobname = request.args.get('jobname', type=str)
    #     pass

    
    @app.route('/api/v2/jobs/keyword', methods = ['POST'])
    def specific_jobs():
        reqJSON = request.get_json()

        global keyword
        keyword = reqJSON['keyword']

        return dbcons.get_specific_job(tableName=os.environ.get('TABLENAME'))

    return app
    