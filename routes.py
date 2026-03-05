from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import Booking, Package  # Fixed: Package (singular), not Packages
from . import bookings_bp
from datetime import datetime

@bookings_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

@bookings_bp.route('/create/<int:package_id>', methods=['GET', 'POST'])
@login_required
def create_booking(package_id):
    package = Package.query.get_or_404(package_id)
    if request.method == 'POST':
        travel_date = datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        guests = int(request.form.get('guests'))
        special_requests = request.form.get('special_requests')
        booking = Booking(
            user_id=current_user.id,
            package_id=package.id,
            travel_date=travel_date,
            guests=guests,
            special_requests=special_requests,
            status='pending'
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking created successfully!', 'success')
        return redirect(url_for('bookings.my_bookings'))
    return render_template('create_booking.html', package=package, now=datetime.now)

@bookings_bp.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        booking.travel_date = datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        booking.guests = int(request.form.get('guests'))
        booking.special_requests = request.form.get('special_requests')
        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('bookings.my_bookings'))
    return render_template('edit_booking.html', booking=booking)

@bookings_bp.route('/delete/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking cancelled.', 'info')
    return redirect(url_for('bookings.my_bookings'))