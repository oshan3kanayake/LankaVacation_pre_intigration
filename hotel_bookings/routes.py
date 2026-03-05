from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import HotelBooking, Hotel
from . import hotel_bp
from datetime import datetime

@hotel_bp.route('/my-hotel-bookings')
@login_required
def my_hotel_bookings():
    bookings = HotelBooking.query.filter_by(user_id=current_user.id).order_by(HotelBooking.check_in.desc()).all()
    return render_template('my_hotel_bookings.html', bookings=bookings)

@hotel_bp.route('/create/<int:hotel_id>', methods=['GET', 'POST'])
@login_required
def create_hotel_booking(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if request.method == 'POST':
        check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%d').date()
        check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%d').date()
        rooms = int(request.form.get('rooms'))
        total_price = float(request.form.get('total_price'))

        if check_out <= check_in:
            flash('Check-out date must be after check-in date.', 'danger')
            return redirect(url_for('hotel.create_hotel_booking', hotel_id=hotel.id))

        booking = HotelBooking(
            user_id=current_user.id,
            hotel_id=hotel.id,
            check_in=check_in,
            check_out=check_out,
            rooms=rooms,
            total_price=total_price,
            status='pending'
        )
        db.session.add(booking)
        db.session.commit()
        flash('Hotel booking created!', 'success')
        return redirect(url_for('hotel.my_hotel_bookings'))
    return render_template('create_hotel_booking.html', hotel=hotel, now=datetime.now)

@hotel_bp.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_hotel_booking(booking_id):
    booking = HotelBooking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        booking.check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%d').date()
        booking.check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%d').date()
        booking.rooms = int(request.form.get('rooms'))
        booking.total_price = float(request.form.get('total_price'))
        if booking.check_out <= booking.check_in:
            flash('Check-out date must be after check-in date.', 'danger')
            return redirect(url_for('hotel.edit_hotel_booking', booking_id=booking.id))
        db.session.commit()
        flash('Hotel booking updated!', 'success')
        return redirect(url_for('hotel.my_hotel_bookings'))
    return render_template('edit_hotel_booking.html', booking=booking)

@hotel_bp.route('/delete/<int:booking_id>', methods=['POST'])
@login_required
def delete_hotel_booking(booking_id):
    booking = HotelBooking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    flash('Hotel booking deleted.', 'info')
    return redirect(url_for('hotel.my_hotel_bookings'))