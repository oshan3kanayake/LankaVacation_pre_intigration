from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from extensions import db
from models import Review, Package
from . import reviews_bp
from datetime import datetime

BAD_WORDS = ['bad', 'awful', 'terrible', 'worst', 'stupid', 'hate', 'dumb', 'shit', 'fuck', 'damn']

def contains_bad_words(text):
    if not text:
        return False
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False

@reviews_bp.route('/create/<int:package_id>', methods=['GET', 'POST'])
@login_required
def create_review(package_id):
    package = Package.query.get_or_404(package_id)
    existing_review = Review.query.filter_by(user_id=current_user.id, package_id=package.id).first()
    if existing_review:
        flash('You have already reviewed this package. You can edit your existing review.', 'warning')
        return redirect(url_for('reviews.edit_review', review_id=existing_review.id))
    if request.method == 'POST':
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment').strip()
        if contains_bad_words(comment):
            flash('Your review contains inappropriate language. Please revise.', 'danger')
            return redirect(url_for('reviews.create_review', package_id=package.id))
        review = Review(
            user_id=current_user.id,
            package_id=package.id,
            rating=rating,
            comment=comment,
            is_approved=True
        )
        db.session.add(review)
        db.session.commit()
        flash('Your review has been posted!', 'success')
        return redirect(url_for('packages.package_detail', package_id=package.id))
    return render_template('create_review.html', package=package)

@reviews_bp.route('/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        review.rating = int(request.form.get('rating'))
        review.comment = request.form.get('comment').strip()
        if contains_bad_words(review.comment):
            flash('Your review contains inappropriate language. Please revise.', 'danger')
            return redirect(url_for('reviews.edit_review', review_id=review.id))
        db.session.commit()
        flash('Your review has been updated!', 'success')
        return redirect(url_for('packages.package_detail', package_id=review.package_id))
    return render_template('edit_review.html', review=review)

@reviews_bp.route('/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)
    package_id = review.package_id
    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted.', 'info')
    return redirect(url_for('packages.package_detail', package_id=package_id))