''' API token management '''
from flask import Blueprint, render_template

VIEW_TOKEN = Blueprint('token', __name__, url_prefix='/token')

@VIEW_TOKEN.route('/', methods=('GET',))
def index() -> str:
    ''' index page '''
    return render_template('settings_token.html')
