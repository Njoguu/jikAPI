from flask import Blueprint, request, render_template, abort
import os, sys
path = os.getcwd()
sys.path.append(path+"/src/")
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import hashlib
import logging
import requests
import json
from dotenv import load_dotenv

load_dotenv()

newsletter = Blueprint("newsletter", __name__, url_prefix="/api/v2/newsletter")

mailchimp = Client()
mailchimp.set_config({
    'api_key': os.environ['MAILCHIMP_API_KEY'],
    'server': os.environ['MAILCHIMP_REGION'],
})

logger = logging.getLogger(__name__)

# Recaptcha setup
recaptcha_API_secret_key = os.environ['RECAPTCHA_API_SECRET_KEY']
verify_url = 'https://www.google.com/recaptcha/api/siteverify'
recaptcha_API_key = os.environ['RECAPTCHA_API_KEY']

@newsletter.route('/subscribe', methods=['POST'])
def subscribe():
    # add the email address to your mailing list here
    if request.method == 'POST':
        try:
            email = request.form['email']
            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(url=f'{verify_url}?secret={recaptcha_API_secret_key}&response={secret_response}').json()
            if verify_response['success'] == False:
                abort(401)
            else:
                form_email_hash = hashlib.md5(email.encode('utf-8').lower()).hexdigest()
                member_update = {
                    'status': 'subscribed',
                }
                response = mailchimp.lists.set_list_member(
                    os.environ['MAILCHIMP_MARKETING_AUDIENCE_ID'],
                    form_email_hash,
                    member_update,
                )
                logger.info(f'API call successful: {response}')
                data = '{"title": "Successfully subscribed!","message": "You have been successfully subscribed to our mailing list."}'
                json_data = json.loads(data)
                return render_template('message.html', json_data=json_data)

        except ApiClientError as error:
            logger.error(f'An exception occurred: {error.text}')
            data = data = '{"title": "Failed to subscribe!","message": "Oops, something went wrong."}'
            json_data = json.loads(data)
            return render_template('message.html', json_data=json_data)

@newsletter.route('/unsubscribe', methods=['GET','POST'])
def unsubscribe():
    if request.method == 'POST':
        try:
            email = request.form['email']
            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(url=f'{verify_url}?secret={recaptcha_API_secret_key}&response={secret_response}').json()
            if verify_response['success'] == False:
                abort(401)
            else:
                form_email_hash = hashlib.md5(email.encode('utf-8').lower()).hexdigest()
                member_update = {
                    'status': 'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    os.getenv('MAILCHIMP_MARKETING_AUDIENCE_ID'),
                    form_email_hash,
                    member_update,
                )
                logger.info(f'API call successful: {response}')
                data = '{"title": "Successfully unsubscribed!","message": "You have been successfully unsubscribed from our mailing list."}'
                json_data = json.loads(data)
                return render_template('message.html', json_data=json_data)

        except ApiClientError as error:
            logger.error(f'An exception occurred: {error.text}')
            data = data = '{"title": "Failed to unsubscribe!","message": "Oops, something went wrong. Could not subscribe you to our mailing list."}'
            json_data = json.loads(data)
            return render_template('message.html', json_data=json_data)

    return render_template('unsubscribe.html', site_key=recaptcha_API_key)

#  # TODO --> SEND PING TO TESTS
#     @newsl.route('/api/mailchimp/ping')
#     def mailchimp_ping_view():
#         response = mailchimp.ping.get()
#         return jsonify(response)