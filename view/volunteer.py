'''
API for COSCUP-Volunteer
'''
from flask import Blueprint

VIEW_VOLUNTEER = Blueprint('volunteer', __name__, url_prefix='/coscup')
