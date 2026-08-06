from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import quote
from app.models.user_models import User
from app.models.trek_models import Trek
from app.forms.auth_forms import LoginForm, RegistrationForm
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def landing():
    treks = Trek.query.filter(Trek.status == 'open').order_by(Trek.start_date).limit(6).all()
    destinations = [
        {'name': 'Machu Picchu', 'region': 'Peru', 'highlight': 'Ancient Incan citadel above the cloud forest'},
        {'name': 'Patagonia', 'region': 'Argentina / Chile', 'highlight': 'Epic glaciers and mountain wilderness'},
        {'name': 'Dolomites', 'region': 'Italy', 'highlight': 'Jagged alpine ridges and scenic hikes'},
        {'name': 'Banff National Park', 'region': 'Canada', 'highlight': 'Turquoise lakes and rugged peaks'},
        {'name': 'Kilimanjaro', 'region': 'Tanzania', 'highlight': 'Africa’s highest trekable summit'},
        {'name': 'South Island', 'region': 'New Zealand', 'highlight': 'Fiords, lakes, and geothermal scenery'},
        {'name': 'Grand Canyon', 'region': 'USA', 'highlight': 'World-famous canyon rim trails'},
        {'name': 'Mount Fuji', 'region': 'Japan', 'highlight': 'Iconic volcanic summit and sacred views'},
        {'name': 'Inca Trail', 'region': 'Peru', 'highlight': 'Historic trek to a legendary ruin'},
        {'name': 'Annapurna Circuit', 'region': 'Nepal', 'highlight': 'High Himalayan passes and village culture'},
        {'name': 'Everest Base Camp', 'region': 'Nepal', 'highlight': 'Gateway to the highest mountain on Earth'},
        {'name': 'Torres del Paine', 'region': 'Chile', 'highlight': 'Granite towers and Patagonian steppe'},
        {'name': 'Cinque Terre', 'region': 'Italy', 'highlight': 'Coastal trails and colorful cliffside villages'},
        {'name': 'Zion National Park', 'region': 'USA', 'highlight': 'Canyons, slot hikes, and red rock vistas'},
        {'name': 'Swiss Alps', 'region': 'Switzerland', 'highlight': 'Classic alpine trekking with village charm'},
        {'name': 'Yosemite', 'region': 'USA', 'highlight': 'Granite monoliths and forested valleys'},
        {'name': 'Mount Batur', 'region': 'Indonesia', 'highlight': 'Sunrise volcano hike with lake views'},
        {'name': 'Lofoten Islands', 'region': 'Norway', 'highlight': 'Arctic fjords and dramatic coastal terrain'},
        {'name': 'Sahara Desert', 'region': 'Morocco', 'highlight': 'Dunes, desert camps, and starry nights'},
        {'name': 'Great Wall', 'region': 'China', 'highlight': 'Historic fortification ridge hikes'},
        {'name': 'Isle of Skye', 'region': 'Scotland', 'highlight': 'Mystical landscapes and rugged peninsulas'},
        {'name': 'Trolltunga', 'region': 'Norway', 'highlight': 'Dramatic cliff viewpoint over a fjord'},
        {'name': 'The Himalayas', 'region': 'India/Nepal/Bhutan', 'highlight': 'High-altitude trails and spiritual mountains'},
        {'name': 'Table Mountain', 'region': 'South Africa', 'highlight': 'Panoramic city and ocean views'},
        {'name': 'Mount Rainier', 'region': 'USA', 'highlight': 'Glacier-carved slopes and wildflower meadows'},
        {'name': 'Masai Mara', 'region': 'Kenya', 'highlight': 'Savannah safaris and wildlife treks'},
        {'name': 'Aoraki Mount Cook', 'region': 'New Zealand', 'highlight': 'Southern Alps peak and glacier hikes'},
        {'name': 'The Dolomites', 'region': 'Italy', 'highlight': 'Historic alpine trails and UNESCO scenery'},
        {'name': 'Arches National Park', 'region': 'USA', 'highlight': 'Natural stone arches and desert paths'},
        {'name': 'Fiordland', 'region': 'New Zealand', 'highlight': 'Dramatic fiord-land wilderness treks'},
        {'name': 'Patagonian Ice Fields', 'region': 'Argentina / Chile', 'highlight': 'Expansive ice and rugged mountain adventure'}
    ]
    for destination in destinations:
        destination['wiki_url'] = 'https://en.wikipedia.org/wiki/' + quote(destination['name'].replace(' ', '_'))
    return render_template('landing.html', treks=treks, destinations=destinations)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data) and user.status == 'active':
            login_user(user)
            flash('Welcome back to Trekspire!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        flash('Invalid credentials or account inactive.', 'danger')
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if existing:
            flash('Email already exists. Try signing in.', 'warning')
        else:
            user = User(full_name=form.full_name.data.strip(), email=form.email.data.lower().strip())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created. Sign in to begin your next trek.', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.landing'))

@main_bp.route('/home')
@login_required
def home():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    if current_user.is_staff():
        return redirect(url_for('staff.dashboard'))
    return redirect(url_for('user.dashboard'))

@main_bp.route('/treks')
def trek_list():
    location = request.args.get('location', '').strip()
    difficulty = request.args.get('difficulty', '')
    duration = request.args.get('duration', '')
    price = request.args.get('price', '')
    query = Trek.query.filter(Trek.status == 'open')
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if duration:
        query = query.filter(Trek.duration.ilike(f'%{duration}%'))
    if price:
        try:
            price_limit = float(price)
            query = query.filter(Trek.price <= price_limit)
        except ValueError:
            pass
    treks = query.order_by(Trek.start_date).all()
    return render_template('trek_list.html', treks=treks)

@main_bp.route('/trek/<int:trek_id>')
def trek_detail(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    from app.forms.auth_forms import BookingForm
    book_form = BookingForm()
    return render_template('trek_detail.html', trek=trek, book_form=book_form)

