from flask import Blueprint, jsonify, request
from http.client import BAD_REQUEST, CREATED, NO_CONTENT, OK, INTERNAL_SERVER_ERROR
import os, sys
path = os.getcwd()
sys.path.append(path+"/src/")
from backend import database as dbcons
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from dotenv import load_dotenv

load_dotenv()

postings = Blueprint("postings", __name__, url_prefix="")

# Route to retrieve the list of available jobs
@postings.route('/api/v2/jobs', methods=['GET'])
@swag_from('./docs/postings/jobs.yaml')     #--> Use the 'swag_from' decorator to document this endpoint in the Swagger UI
def available_jobs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 25, type=int)

        data = dbcons.getData(tableName=os.environ['TABLENAME'])
        jobs = data[0][0]

        # Determine the total number of pages
        total_pages = (len(jobs) + per_page - 1) // per_page

        # Get the slice of data for the current page
        start = (page - 1) * per_page
        end = start + per_page
        current_page_data = jobs[start:end]
        prev = page-1
        if prev == 0:
            prev = None
        next = page+1
        if next > total_pages:
            next = None

        meta = {
            'current_page' : page,
            'total_pages' : total_pages,
            'total_job_count' : len(jobs),
            'previous_page': prev,
            'next_page': next,

        }

        if len(jobs) == 0:
            return jsonify({"error": "No jobs found"}), NO_CONTENT
        else:
            return jsonify({
                'Available jobs' : current_page_data,
                'meta' : meta
            }), OK
    except IndexError as err:
        return jsonify({"error": "Unexpected data format"}), INTERNAL_SERVER_ERROR
    except Exception as err:
        return jsonify({"error": "An unexpected error has occurred"}), INTERNAL_SERVER_ERROR

# Route to post new available jobs
@postings.route('/api/v2/jobs', methods=['POST'])
@swag_from('./docs/postings/add_new_opening.yaml')
def add_new_job():
    try:
        # jobs = dbcons.getData(tableName=environ['TABLENAME'))[0][0]
        job = request.get_json()
        # jobs.append(request_data)
        dbcons.addData(job, tableName=os.environ['TABLENAME'])
        return jsonify({"message": "Job created successfully", "job":job}), CREATED
    except Exception as err:
        print(err)

# Route to update already available jobs with a specific ID
@postings.route('/api/v2/jobs/<int:id>', methods=['PATCH'])
@jwt_required()
@swag_from('./docs/postings/update_job_by_id.yaml')
def update_job_by_id(id):
    try:
        data = dbcons.getData(tableName=os.environ['TABLENAME'])
        jobs = data[0][0]
        job = next((job for job in jobs if job['id'] == id), None)
        if job:
            request_data = request.get_json()
            jobname = request_data.get('jobname')
            joburl = request_data.get('joburl')
            dbcons.updateData(jobname, joburl, id=job['id'], tableName=os.environ['TABLENAME'])
            return jsonify({"message": "Job updated"}), OK
        else:
            return jsonify({"error": "Job not found"}), NO_CONTENT
    except Exception as err:
        print(err)

# Route to search for a job with a specific ID
@postings.route('/api/v2/jobs/<int:id>', methods=['GET'])
@swag_from('./docs/postings/get_job_by_id.yaml')
def get_by_id(id):
    try:
        data = dbcons.getData(tableName=os.environ['TABLENAME'])
        jobs = data[0][0]
        job = next((job for job in jobs if job['id'] == id), None)
        if job:
            return jsonify(job), OK
        else:
            return jsonify({"error": "Job not found"}), NO_CONTENT
    except Exception as err:
        print(err)

# Route to delete a job with a specific ID
@postings.route('/api/v2/jobs/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from('./docs/postings/delete_job_by_id.yaml')
def delete_by_id(id):
    try:
        data = dbcons.getData(tableName=os.environ['TABLENAME'])
        jobs = data[0][0]
        job = next((job for job in jobs if job['id'] == id), None)
        if job:
            dbcons.deleteData(id=job['id'], tableName=os.environ['TABLENAME'])
            return jsonify({"message": "Job deleted successfully"}), OK
        else:
            return jsonify({"error": "Job not found"}), NO_CONTENT
    except Exception as err:
        print(err)
    
# Using Query parameters
# /api/v2/jobs/keyword?jobname=Software+Developer
@postings.route('/api/v2/jobs/keyword')
def qspecific_jobs():
    keyword = request.args.get('jobname', '', type=str)

    data = dbcons.get_specific_job(keywords=keyword, tableName=os.environ['TABLENAME'])
    jobs = data[0][0]
    return jsonify(jobs)

# Route to find a job with specific keywords
@postings.route('/api/v2/jobs/keyword', methods = ['POST'])
@swag_from('./docs/postings/use_keyword.yaml')
def specific_jobs():
    try: 
        reqJSON = request.get_json()
        keyword = reqJSON.get("keyword")

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 15, type=int)

        if keyword is None:
            return jsonify({'error': 'keyword is a required field'})
        try:
            data = dbcons.get_specific_job(keywords=keyword, tableName=os.environ['TABLENAME'])
            jobs = data[0][0]

            # Determine the total number of pages
            total_pages = (len(jobs) + per_page - 1) // per_page

            # Get the slice of data for the current page
            start = (page - 1) * per_page
            end = start + per_page
            current_page_data = jobs[start:end]
            prev = page-1
            if prev == 0:
                prev = None
            next = page+1
            if next > total_pages:
                next = None

            meta = {
                'current_page' : page,
                'total_pages' : total_pages,
                'total_job_count' : len(jobs),
                'previous_page': prev,
                'next_page': next,

            }
            if len(jobs) == 0:
                return jsonify({"error": "No jobs found"}), NO_CONTENT
            else:
                return jsonify({
                    'Available jobs' : current_page_data,
                    'meta' : meta
                }), OK
        except Exception as err:
            print(err)
            return jsonify({'error': 'An error occurred while retrieving the job data'}), NO_CONTENT
    except BAD_REQUEST as err:
        return jsonify({'error': 'The request body must contain valid JSON data'})

# Route to find a job posted on a specific date
@postings.route('/api/v2/jobs/date', methods=['POST'])
@swag_from('./docs/postings/use_date.yaml')
def date_specified():
    try:
        reqJSON = request.get_json()
        specified_date = reqJSON['specified_date']
        if specified_date is None:
            return jsonify({'error': 'specified_date is a required field'})
        try:
            data = dbcons.get_job_of_specific_date(specified_dates=specified_date, tableName=os.environ['TABLENAME'])
            jobs = data[0][0]
            if len(jobs) == 0:
                return jsonify({"error": "No jobs found"}), NO_CONTENT
            else:
                return jsonify(jobs), OK
        except Exception as err:
            print(err)
            return jsonify({'error': 'An error occurred while retrieving the job data'}), INTERNAL_SERVER_ERROR
    except BAD_REQUEST as err:
        return jsonify({'error': 'The request body must contain valid JSON data'})

