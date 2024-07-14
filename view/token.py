''' API token management '''
from flask import Blueprint, Response, make_response, render_template, request, jsonify
from werkzeug.exceptions import BadRequest

from module.api_token import APIToken

VIEW_TOKEN = Blueprint('token', __name__, url_prefix='/token')

@VIEW_TOKEN.errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> Response:
    return make_response({ 'message': e.description }, e.code)

@VIEW_TOKEN.route('/', methods=('GET',))
def index() -> str:
    ''' index page '''
    return render_template('settings_token.html')

@VIEW_TOKEN.route('/', methods=('POST',))
def create_token() -> str | Response:
    '''API for creating token

    Request Body: 
    {
        "label": string
    }

    Response Body (200):
    {
        "label": string,
        "token": string,
    }
    '''
    create_token_dto = request.get_json()

    if 'label' not in create_token_dto or \
        type(create_token_dto['label']) is not str or \
        len(create_token_dto['label']) == 0:
        raise BadRequest('label should not be empty string.')

    new_token = APIToken.create(create_token_dto['label'])
    return jsonify({
        'label': new_token.label,
        'token': new_token.token,
    })

@VIEW_TOKEN.route('/list', methods=('GET',))
def get_list() -> Response:
    tokens = APIToken.get_list()
    return jsonify({ 'tokens': tokens })

@VIEW_TOKEN.route('/', methods=('DELETE',))
def delete() -> Response:
    delete_token_dto = request.get_json()

    if not isinstance(delete_token_dto['tokens'], list):
        raise BadRequest('tokens should be in the body and an array of string')
    
    for token in delete_token_dto['tokens']:
        if type(token) is not str:
            raise BadRequest('tokens should be an array of string')
        
    APIToken.delete(delete_token_dto['tokens'])
        
    return jsonify({ 'success': True })
