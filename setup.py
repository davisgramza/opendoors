from werkzeug.security import generate_password_hash

from models import *
from validations import NotificationIdentifiers


def setup():
    administrator = Administrator(username='opendoors', hash=generate_password_hash('lakeforest'))
    db.session.add(administrator)
    settings = Configuration(program_status='Active', email=False)
    db.session.add(settings)
    mentor = Mentor(mentor_name='a', category='a', description='a', special_instructions='a', contact_name='a',
                    phone='a', email='opendoorsdemo@gmail.com', address='a', students=8, status=True)
    op1 = Opportunity(date='2002-11-17', session='am', mentor=mentor)
    op2 = Opportunity(date='1999-11-17', session='pm', mentor=mentor)
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

    student = Student(last_name='a', first_name='a', address='a', home_phone='a', cell_phone='a',
                      student_email='opendoorsdemo@gmail.com', parent_email='a@b.com', lunch_period='A',
                      graduation_year='2021', approved=True, opportunity=op1)
    student2 = Student(last_name='a', first_name='a', address='a', home_phone='a', cell_phone='a',
                       student_email='opendoorsdemo@gmail.com', parent_email='a@b.com', lunch_period='A',
                       graduation_year='2021', approved=True, opportunity=op1)
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
    db.session.add(mentor)
    db.session.add(op1)
    db.session.add(op2)
    db.session.add(student)
    db.session.add(student2)
    db.session.commit()
