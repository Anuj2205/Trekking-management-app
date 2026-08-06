from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.trek_models import Trek
from app.models.booking_models import Booking
from app.models.user_models import User

staff_bp = Blueprint('staff', __name__)

def staff_only(view):
    from functools import wraps
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff():
            flash('Access denied.', 'danger')
            return redirect(url_for('main.login'))
        return view(*args, **kwargs)
    return wrapped

@staff_bp.route('/dashboard')
@login_required
@staff_only
def dashboard():
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    upcoming = [trek for trek in assigned_treks if trek.start_date >= date.today()]
    participants = Booking.query.join(Trek).filter(Trek.assigned_staff_id == current_user.id).count()
    return render_template('staff/dashboard.html', assigned_treks=assigned_treks, upcoming=upcoming, participants=participants)

@staff_bp.route('/trek/<int:trek_id>/update', methods=['GET', 'POST'])
@login_required
@staff_only
def update_trek_status(trek_id):
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()
    if request.method == 'POST':
        trek.status = request.form.get('status', trek.status)
        trek.available_slots = int(request.form.get('available_slots', trek.available_slots))
        db.session.commit()
        flash('Trek status updated.', 'success')
        return redirect(url_for('staff.dashboard'))
    return render_template('staff/update_trek.html', trek=trek)

@staff_bp.route('/trek/<int:trek_id>/participants')
@login_required
@staff_only
def participants(trek_id):
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()
    participants = Booking.query.filter_by(trek_id=trek.id).all()
    return render_template('staff/participants.html', trek=trek, participants=participants)
