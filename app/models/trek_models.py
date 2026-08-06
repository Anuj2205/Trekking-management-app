from datetime import date
from app import db

class Trek(db.Model):
    __tablename__ = 'treks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(30), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_staff = db.relationship('User', foreign_keys=[assigned_staff_id], backref='assigned_treks')
    status = db.Column(db.String(30), default='open', nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    bookings = db.relationship('Booking', backref='trek', lazy=True)

    def is_open(self):
        return self.status == 'open' and self.available_slots > 0 and self.start_date >= date.today()
