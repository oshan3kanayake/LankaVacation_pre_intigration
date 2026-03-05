from flask import Blueprint

hotel_bp = Blueprint('hotel', __name__, template_folder='templates/hotel_bookings')

from . import routes