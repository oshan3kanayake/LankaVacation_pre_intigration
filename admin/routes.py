from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from extensions import db
from models import User, Ticket, TicketReply, Booking, HotelBooking, Package, Hotel
from . import admin_bp
from datetime import datetime, timedelta
import random
from functools import wraps

# Admin role check decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Admin login page
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = User.query.filter_by(email=username, role='admin').first()
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid admin credentials', 'danger')
    return render_template('admin_login.html')

@admin_bp.route('/logout')
@login_required
@admin_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    revenue_data = [random.randint(5000, 15000) for _ in range(12)]

    total_users = User.query.count()
    total_bookings = Booking.query.count() + HotelBooking.query.count()
    total_tickets = Ticket.query.count()
    total_packages = Package.query.count()
    total_hotels = Hotel.query.count()

    popular_packages = db.session.query(
        Package.title, db.func.count(Booking.id).label('count')
    ).outerjoin(Booking).group_by(Package.id).order_by(db.desc('count')).limit(3).all()

    popular_hotels = db.session.query(
        Hotel.name, db.func.count(HotelBooking.id).label('count')
    ).outerjoin(HotelBooking).group_by(Hotel.id).order_by(db.desc('count')).limit(3).all()

    from models import Review
    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()

    return render_template('dashboard.html',
                           months=months,
                           revenue_data=revenue_data,
                           total_users=total_users,
                           total_bookings=total_bookings,
                           total_tickets=total_tickets,
                           total_packages=total_packages,
                           total_hotels=total_hotels,
                           popular_packages=popular_packages,
                           popular_hotels=popular_hotels,
                           recent_tickets=recent_tickets)

@admin_bp.route('/reviews')
@login_required
@admin_required
def reviews():
    from models import Review
    all_reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin_reviews.html', reviews=all_reviews)

@admin_bp.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_review(review_id):
    from models import Review
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review has been deleted.', 'info')
    return redirect(url_for('admin.reviews'))

# Tickets list with optional filter
@admin_bp.route('/tickets')
@login_required
@admin_required
def tickets():
    filter_type = request.args.get('filter', 'all')  # 'all', 'replied', 'unreplied'
    if filter_type == 'replied':
        # Tickets that have at least one reply
        tickets = Ticket.query.join(Ticket.replies).distinct().order_by(Ticket.created_at.desc()).all()
    elif filter_type == 'unreplied':
        # Tickets that have no replies
        tickets = Ticket.query.outerjoin(Ticket.replies).filter(TicketReply.id == None).order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('tickets.html', tickets=tickets, current_filter=filter_type)

@admin_bp.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == 'POST':
        reply_text = request.form.get('reply').strip()
        if reply_text:
            reply = TicketReply(
                ticket_id=ticket.id,
                admin_id=current_user.id,
                reply=reply_text
            )
            db.session.add(reply)
            db.session.commit()
            flash('Reply added.', 'success')
        return redirect(url_for('admin.ticket_detail', ticket_id=ticket.id))
    return render_template('admin_ticket_detail.html', ticket=ticket)

# Update status and redirect to dashboard (as requested)
@admin_bp.route('/ticket/<int:ticket_id>/status/<string:status>')
@login_required
@admin_required
def update_ticket_status(ticket_id, status):
    ticket = Ticket.query.get_or_404(ticket_id)
    if status in ['open', 'closed', 'resolved']:
        ticket.status = status
        db.session.commit()
        flash(f'Ticket marked as {status}.', 'success')
    return redirect(url_for('admin.dashboard'))  # Now redirects to dashboard

@admin_bp.route('/reply/edit/<int:reply_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_reply(reply_id):
    reply = TicketReply.query.get_or_404(reply_id)
    if reply.admin_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        reply.reply = request.form.get('reply').strip()
        db.session.commit()
        flash('Reply updated.', 'success')
        return redirect(url_for('admin.ticket_detail', ticket_id=reply.ticket_id))
    return render_template('edit_reply.html', reply=reply)

@admin_bp.route('/reply/delete/<int:reply_id>')
@login_required
@admin_required
def delete_reply(reply_id):
    reply = TicketReply.query.get_or_404(reply_id)
    if reply.admin_id != current_user.id:
        abort(403)
    ticket_id = reply.ticket_id
    db.session.delete(reply)
    db.session.commit()
    flash('Reply deleted.', 'info')
    return redirect(url_for('admin.ticket_detail', ticket_id=ticket_id))