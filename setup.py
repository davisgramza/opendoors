from werkzeug.security import generate_password_hash
import os

from app import db
from models import *
from validations import NotificationIdentifiers


def setup():
    db.create_all()
    if os.environ.get('RESET'):
        db.drop_all()
        db.create_all()
    if not Administrator.query.first():
        administrator = Administrator(username=os.getenv('ADMINISTRATOR_USERNAME'), hash=generate_password_hash(os.getenv('ADMINISTRATOR_PASSWORD')))
        db.session.add(administrator)
    if not Configuration.query.first():
        settings = Configuration(program_status='Active', email=False)
        db.session.add(settings)
    if not Notification.query.first():
        enabled = Notification(identifier=NotificationIdentifiers.PROGRAM_ACTIVE,
                               description='The message that students will see on the landing page when the program is active',
                               message='The program is active.')
        preview = Notification(identifier=NotificationIdentifiers.PROGRAM_PREVIEW,
                               description='The message that students will see on the landing page when the program is preview',
                               message='The program is preview.')
        disabled = Notification(identifier=NotificationIdentifiers.PROGRAM_DISABLED,
                                description='The message that students will see on the landing page when the program is disabled',
                                message='The program is disabled.')
        disclaimer = Notification(identifier=NotificationIdentifiers.DISCLAIMER,
                                  description='The message that will be shown for a student that is registering. Will have to agree to this when registering',
                                  message='You must agree to the terms of Open Doors.')
        submission = Notification(identifier=NotificationIdentifiers.SUBMISSION_TEXT,
                                  description='The text that appears after the student registers for an opportunity. Will be displayed on screen and emailed to the student.',
                                  message='Thank you for registering')
        approval = Notification(identifier=NotificationIdentifiers.APPROVAL,
                                description='The text of the email that is sent to the student if approved',
                                message='Congratulations!')
        denied = Notification(identifier=NotificationIdentifiers.DENIED,
                              description='The text of the email that is sent to the student if denied', message='Sorry')
        deleted = Notification(identifier=NotificationIdentifiers.DELETED,
                               description='The text of the emailthat is sent to the student if deleted',
                               message='You have been deleted.')
        registration_fields = Notification(identifier=NotificationIdentifiers.REGISTRATION_FIELDS,
                                           description='The disclaimer that is shown to students upon registration',
                                           message='All fields are required')
        mentor_notification = Notification(identifier=NotificationIdentifiers.MENTOR_NOTIFICATION,
                                           description='The message that is sent to students signed up for notifications when an opportunity for a mentor that they register opens up.',
                                           message='An opportunity is now available')
        db.session.add(enabled)
        db.session.add(preview)
        db.session.add(disabled)
        db.session.add(disclaimer)
        db.session.add(submission)
        db.session.add(approval)
        db.session.add(denied)
        db.session.add(deleted)
        db.session.add(registration_fields)
        db.session.add(mentor_notification)
    db.session.commit()
