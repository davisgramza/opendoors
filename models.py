from flask_login import UserMixin
from sqlalchemy import func

from app import db


class Administrator(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_name = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    special_instructions = db.Column(db.Text, nullable=False)
    contact_name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    students = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    waitlist_active = db.Column(db.Boolean, default=False, nullable=False)

    opportunities = db.relationship('Opportunity', backref='mentor', lazy=True, cascade='all, delete',
                                    order_by='Opportunity.date.asc()')
    notifications = db.relationship('MentorNotification', backref='mentor', lazy=True, cascade='all, delete')


class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    session = db.Column(db.Text, nullable=False)

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)
    students = db.relationship('Student', backref='opportunity', lazy=True, cascade='all, delete',
                               order_by='Student.last_name.asc(), Student.first_name.asc()')


class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_status = db.Column(db.Text, nullable=False)
    email = db.Column(db.Boolean, nullable=False)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    home_phone = db.Column(db.Text, nullable=False)
    cell_phone = db.Column(db.Text, nullable=False)
    student_email = db.Column(db.Text, nullable=False)
    parent_email = db.Column(db.Text, nullable=False)
    lunch_period = db.Column(db.Text, nullable=False)
    graduation_year = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, nullable=False, default=False)
    registration_time = db.Column(db.Text, nullable=False, default=func.now())

    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)


class MentorNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)

    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'), nullable=False)
