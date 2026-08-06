from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models.user_models import User
from app.models.trek_models import Trek
from app.models.booking_models import Booking
from app.models.staff_models import StaffProfile
from app.forms.trek_forms import TrekForm

admin_bp = Blueprint('admin', __name__)

def admin_only(view):
    from functools import wraps
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied.', 'danger')
            return redirect(url_for('main.login'))
        return view(*args, **kwargs)
    return wrapped

@admin_bp.route('/dashboard')
@login_required
@admin_only
def dashboard():
    query = request.args.get('q', '').strip()
    total_treks = Trek.query.count()
    total_users = User.query.filter(User.role == 'user').count()
    total_staff = User.query.filter(User.role == 'staff').count()
    total_bookings = Booking.query.count()
    trend_data = [Booking.query.filter(Booking.booking_date >= date.today()).count(), Booking.query.count()]
    pending_staff = StaffProfile.query.filter_by(approval_status='pending').all()
    searched = None
    search_results = {}
    if query:
        searched = query
        search_results['treks'] = Trek.query.filter(
            (Trek.title.ilike(f'%{query}%')) | (Trek.location.ilike(f'%{query}%'))
        ).all()
        search_results['users'] = User.query.filter(
            (User.full_name.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
        ).all()
        search_results['bookings'] = Booking.query.join(Trek).join(User).filter(
            (Trek.title.ilike(f'%{query}%')) | (User.full_name.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
        ).all()
    return render_template('admin/dashboard.html', total_treks=total_treks,
                           total_users=total_users, total_staff=total_staff,
                           total_bookings=total_bookings, trend_data=trend_data,
                           pending_staff=pending_staff, searched=searched,
                           search_results=search_results)

@admin_bp.route('/treks/new', methods=['GET', 'POST'])
@login_required
@admin_only
def create_trek():
    form = TrekForm()
    staff_users = User.query.filter_by(role='staff').all()
    form.assigned_staff.choices = [(0, 'None')] + [(staff.id, staff.full_name) for staff in staff_users]
    if form.validate_on_submit():
        trek = Trek(
            title=form.title.data.strip(),
            location=form.location.data.strip(),
            difficulty=form.difficulty.data,
            duration=form.duration.data.strip(),
            available_slots=form.available_slots.data,
            price=form.price.data,
            description=form.description.data.strip(),
            image_url=form.image_url.data.strip(),
            status=form.status.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            assigned_staff_id=form.assigned_staff.data or None
        )
        db.session.add(trek)
        db.session.commit()
        flash('Trek created for new natural journeys.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/trek_form.html', form=form, action='New Trek')

@admin_bp.route('/treks/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_only
def edit_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    form = TrekForm(obj=trek)
    staff_users = User.query.filter_by(role='staff').all()
    form.assigned_staff.choices = [(0, 'None')] + [(staff.id, staff.full_name) for staff in staff_users]
    if trek.assigned_staff_id:
        form.assigned_staff.data = trek.assigned_staff_id
    if form.validate_on_submit():
        trek.title = form.title.data.strip()
        trek.location = form.location.data.strip()
        trek.difficulty = form.difficulty.data
        trek.duration = form.duration.data.strip()
        trek.available_slots = form.available_slots.data
        trek.price = form.price.data
        trek.description = form.description.data.strip()
        trek.image_url = form.image_url.data.strip()
        trek.status = form.status.data
        trek.start_date = form.start_date.data
        trek.end_date = form.end_date.data
        trek.assigned_staff_id = form.assigned_staff.data or None
        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/trek_form.html', form=form, action='Edit Trek')

@admin_bp.route('/treks/<int:trek_id>/delete', methods=['POST'])
@login_required
@admin_only
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    flash('Trek removed from the adventure roster.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/staff/approve/<int:staff_id>', methods=['POST'])
@login_required
@admin_only
def approve_staff(staff_id):
    profile = StaffProfile.query.get_or_404(staff_id)
    profile.approval_status = 'approved'
    profile.user.role = 'staff'
    db.session.commit()
    flash('Staff member approved.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/blacklist', methods=['POST'])
@login_required
@admin_only
def blacklist_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot blacklist an admin.', 'danger')
    else:
        user.status = 'blacklisted'
        db.session.commit()
        flash('User has been blacklisted.', 'warning')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/bookings')
@login_required
@admin_only
def booking_history():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin/booking_history.html', bookings=bookings)
