from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    role = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    '''
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }
    '''

class Attendance(db.Model):
    __bind_key__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    pwd = db.Column(db.String(150), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=False, nullable=False)
    name = db.Column(db.String(150), unique=False, nullable=False)
    attendance_time = db.Column(db.DateTime, default=datetime.now)

class CheckinPWD(db.Model):
    __bind_key__ = 'checkinpwd'
    id = db.Column(db.Integer, primary_key=True)
    pwd = db.Column(db.String(150), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
