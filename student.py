import logging
import traceback

from flask import request, render_template, redirect, Blueprint, url_for
from flask_login import login_required

from app import send_mail
from helpers import *
from messages import *
from models import *

student = Blueprint('student', __name__, template_folder='templates')


@student.route('/', methods=['GET'])
def landing():
    configuration = Configuration.query.first()
    notification = Notification.query.filter_by(
        identifier=get_status_from_configuration(configuration.program_status)).first()
    if request.method == 'GET':
        return render_template("student_landing.html", status=configuration.program_status,
                               message=notification.message, success=request.args.get('success'))


@student.route('/register/<mid>', methods=['GET', 'POST'])
def register(mid):
    mentor = Mentor.query.get(mid)
    configuration = Configuration.query.first()
    if not mentor or configuration.program_status != 'Active':
        return redirect(url_for('student.landing'))
    if mentor.waitlist_active:
        return redirect(url_for('student.get_notifications', mid=mid))
    disclaimer = Notification.query.filter_by(identifier=NotificationIdentifiers.DISCLAIMER).first().message
    registration_fields = Notification.query.filter_by(
        identifier=NotificationIdentifiers.REGISTRATION_FIELDS).first().message
    submission = Notification.query.filter_by(identifier=NotificationIdentifiers.SUBMISSION_TEXT).first().message
    if request.method == 'POST':
        error = ''
        try:
            registered_student = get_student_from_form(request, mentor)
            db.session.add(registered_student)
            if mentor_fully_registered(mentor):
                mentor.waitlist_active = True
            db.session.commit()
            send_mail(Message('You Have Applied For a Open Doors Opportunity', body=submission,
                              recipients=[registered_student.student_email]))
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except InvalidEmailException:
            error = Errors.INVALID_EMAIL_ERROR
        except InvalidSelectedOpportunityException:
            error = Errors.INVALID_SELECTED_OPPORTUNITY_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('register.html', error=error, mentor=mentor, format_date=format_date,
                                       get_session=get_session, disclaimer=disclaimer,
                                       registration_fields=registration_fields)
        return redirect(url_for('student.landing', success=submission))
    if request.method == 'GET':
        return render_template('register.html', mentor=mentor, format_date=format_date, get_session=get_session,
                               disclaimer=disclaimer, registration_fields=registration_fields)


@student.route('/view_student/<sid>', methods=['GET'])
@login_required
def view_student(sid):
    viewed_student = Student.query.get(sid)
    if not viewed_student:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('view_student.html', student=viewed_student, format_date=format_date,
                               get_session=get_session)


@student.route('/delete_student/<sid>', methods=['GET', 'POST'])
@login_required
def delete_student(sid):
    deleted_student = Student.query.get(sid)
    approved = deleted_student.approved
    student_email = deleted_student.student_email
    mentor = deleted_student.opportunity.mentor
    if not deleted_student:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'POST':
        error = ''
        try:
            delete_student_from_form(request)
            mentor.waitlist_active = False
            db.session.delete(deleted_student)
            db.session.commit()
            if approved:
                delete_approved_student_message = Notification.query.filter_by(
                    identifier=NotificationIdentifiers.DELETED).first().message
                send_mail(Message('Removed From Open Doors Opportunity', body=delete_approved_student_message,
                                  recipients=[student_email]))
            else:
                denied_student_message = Notification.query.filter_by(
                    identifier=NotificationIdentifiers.DENIED).first().message
                send_mail(Message('Denied From Open Doors Opportunity', body=denied_student_message,
                                  recipients=[student_email]))
            notifications = MentorNotification.query.filter_by(mentor=mentor).all()
            available_opportunity_message = Notification.query.filter_by(
                identifier=NotificationIdentifiers.MENTOR_NOTIFICATION).first().message
            for notification in notifications:
                send_mail(Message('An Opportunity For ' + mentor.mentor_name + ' Is Available',
                                  body=available_opportunity_message + '\n Remember, this opportunity is a first come, first serve basis. To see if this opportunity is available, see if registrations are available on this mentor.',
                                  recipients=[notification.email]))
        except UnconfirmedDeletionException:
            error = Errors.UNCONFIRMED_DELETION_ERRROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('delete_student.html', error=error, student=deleted_student,
                                       format_date=format_date, get_session=get_session)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('delete_student.html', student=deleted_student, format_date=format_date,
                               get_session=get_session)


@student.route('/confirm_student/<sid>', methods=['GET', 'POST'])
@login_required
def confirm_student(sid):
    confirmed_student = Student.query.get(sid)
    if not confirmed_student:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'POST':
        error = ''
        try:
            confirm_student_from_form(request)
            confirmed_student.approved = True
            db.session.commit()
            approved_student_message = Notification.query.filter_by(
                identifier=NotificationIdentifiers.APPROVAL).first().message
            send_mail(Message('Approved For Open Doors Opportunity', body=approved_student_message,
                              recipients=[confirmed_student.student_email, confirmed_student.parent_email]))
        except StudentConfirmationUnconfirmedException:
            error = Errors.STUDENT_CONFIRMATION_UNCONFIRMED_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('confirm_student.html', error=error, student=confirmed_student,
                                       format_date=format_date, get_session=get_session)
        return redirect(url_for('mentor.mentor_schedule', mid=confirmed_student.opportunity.mentor.id))
    if request.method == 'GET':
        return render_template('confirm_student.html', student=confirmed_student, format_date=format_date,
                               get_session=get_session)


@student.route('/unconfirmed_students', methods=['GET', 'POST'])
@login_required
def unconfirmed_students():
    students = Student.query.filter_by(approved=False).all()
    if request.method == 'POST':
        error = ''
        try:
            confirmed_students = get_confirmed_students_from_form(request)
            for confirmed_student in confirmed_students:
                confirmed_student.approved = True
            db.session.commit()
            approved_student_message = Notification.query.filter_by(
                identifier=NotificationIdentifiers.APPROVAL).first().message
            for confirmed_student in confirmed_students:
                send_mail(Message('Approved For Open Doors Opportunity', body=approved_student_message,
                                  recipients=[confirmed_student.student_email, confirmed_student.parent_email]))
        except Exception as e:
            error = 'Unknown error'
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('unconfirmed_students.html', students=students, error=error)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('unconfirmed_students.html', students=students)


@student.route('/get_notifications/<mid>')
def get_notifications(mid):
    mentor = Mentor.query.get(mid)
    if not mentor.waitlist_active:
        return redirect(url_for('mentor.view_mentors'))
    if request.method == 'POST':
        error = ''
        try:
            mentor_notification = get_mentor_notification_from_form(request, mentor)
            db.session.add(mentor_notification)
            db.session.commit()
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except InvalidEmailException:
            error = Errors.INVALID_EMAIL_ERROR
        except DuplicateEmailException:
            error = Errors.DUPLICATE_EMAIL_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('get_notifications.html', error=error, mentor=mentor)
        return redirect(url_for('student.landing', success=Successes.MENTOR_NOTIFICATION_REGISTRATION_SUCCESS))
    if request.method == 'GET':
        return render_template('get_notifications.html', mentor=mentor)
