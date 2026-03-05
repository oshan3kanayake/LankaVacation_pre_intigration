from flask import Blueprint

hotels_bp = Blueprint('hotels', __name__, template_folder='templates/hotels')

from . import routes