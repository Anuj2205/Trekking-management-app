from app import db

class StaffProfile(db.Model):
    __tablename__ = 'staff_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    experience = db.Column(db.String(120), nullable=False)
    certifications = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(30), nullable=False)
    approval_status = db.Column(db.String(30), default='pending', nullable=False)
