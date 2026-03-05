from flask import render_template
from models import Hotel
from . import hotels_bp

@hotels_bp.route('/')
def all_hotels():
    hotels = Hotel.query.all()
    return render_template('all_hotels.html', hotels=hotels)

@hotels_bp.route('/<int:hotel_id>')
def hotel_detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template('hotel_detail.html', hotel=hotel)