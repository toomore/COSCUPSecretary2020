'''
API for COSCUP-Volunteer
'''
import re

from flask import Blueprint, make_response, Response, request
from werkzeug.exceptions import BadRequest

from module.subscriber import Subscriber

VIEW_VOLUNTEER = Blueprint('volunteer', __name__, url_prefix='/volunteer')

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

@VIEW_VOLUNTEER.errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> Response:
    ''' Handle Bad Request exception '''
    return make_response({ 'message': e.description }, e.code)

@VIEW_VOLUNTEER.route('/subscriber', methods=('POST',))
def add_subscriber() -> Response:
    '''API for add subscriber from COSCUP-Volunteer

    Request Body: 
    {
        "name": string,
        "email": string
    }
    '''
    add_subscriber_dto = request.get_json()
    if 'name' not in add_subscriber_dto or \
        not isinstance(add_subscriber_dto['name'], str):
        raise BadRequest('name should be in the request body and string')

    if 'email' not in add_subscriber_dto or \
        not isinstance(add_subscriber_dto['email'], str):
        raise BadRequest('email should be in the request body and string')

    if not EMAIL_REGEX.match(add_subscriber_dto['email']):
        raise BadRequest('The email is not valid')

    Subscriber.process_upload(
        name=add_subscriber_dto['name'],
        mail=add_subscriber_dto['email']
    )

    return make_response({ 'success': True })
