from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.user_models import User
from app.models.trek_models import Trek
from app.models.booking_models import Booking
from app.forms.auth_forms import ProfileForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    recommended = Trek.query.filter(Trek.status == 'open', Trek.price <= 250).order_by(Trek.start_date).limit(3).all()
    upcoming_bookings = Booking.query.filter_by(user_id=current_user.id).join(Trek).filter(Trek.start_date >= date.today()).all()
    return render_template('user/dashboard.html', recommended=recommended, upcoming_bookings=upcoming_bookings)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(full_name=current_user.full_name)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data.strip()
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)

@user_bp.route('/book/<int:trek_id>', methods=['POST'])
@login_required
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if trek.status != 'open' or trek.available_slots <= 0 or trek.start_date < date.today():
        flash('Booking is unavailable for this trek.', 'warning')
        return redirect(url_for('main.trek_detail', trek_id=trek_id))
    existing = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()
    if existing:
        flash('You already have a booking for this trek.', 'info')
        return redirect(url_for('main.trek_detail', trek_id=trek_id))
    booking = Booking(user_id=current_user.id, trek_id=trek_id)
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    flash('Trek booked successfully. Prepare for the expedition.', 'success')
    return redirect(url_for('user.dashboard'))

@user_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first_or_404()
    trek = Trek.query.get(booking.trek_id)
    if trek:
        trek.available_slots += 1
    booking.status = 'canceled'
    db.session.commit()
    flash('Booking canceled. Your slot has been released.', 'info')
    return redirect(url_for('user.dashboard'))
