import logging
import traceback

from flask import request, render_template, redirect, Blueprint, url_for, Response
from flask_login import login_required

from app import send_mail, db
from helpers import *
from messages import Errors

administrator = Blueprint('administrator', __name__, template_folder='templates')


@administrator.route('/landing', methods=['GET'])
@login_required
def administrator_landing():
    if request.method == 'GET':
        return render_template('administrator_landing.html')


@administrator.route('/configuration', methods=['GET', 'POST'])
@login_required
def configuration():
    settings = Configuration.query.first()
    if request.method == 'POST':
        error = ''
        try:
            edit_configuration_from_form(request, settings)
            db.session.commit()
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except InvalidProgramStatusException:
            error = Errors.INVALID_PROGRAM_STATUS_ERROR
        except InvalidEmailNotificationSettingException:
            error = Errors.INVALID_EMAIL_NOTIFICATION_SETTING_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('configuration.html', configuration=settings, error=error)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('configuration.html', configuration=settings)


@administrator.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    messages = Notification.query.all()
    if request.method == 'POST':
        error = ''
        try:
            edit_notifications_from_form(request, messages)
            db.session.commit()
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('notifications.html', notifications=messages, error=error)
        return redirect(url_for('.administrator_landing'))
    if request.method == 'GET':
        return render_template('notifications.html', notifications=messages)


@administrator.route('/reports', methods=['GET'])
@login_required
def reports():
    if request.method == 'GET':
        return render_template('reports.html')


@administrator.route('/student_reports', methods=['GET'])
@login_required
def student_reports():
    if request.method == 'GET':
        students = Student.query.filter_by(approved=True).all()
        return render_template('student_reports.html', students=students, format_date=format_date,
                               get_session=get_session)


@login_required
@administrator.route('/mentor_reports', methods=['GET'])
def mentor_reports():
    if request.method == 'GET':
        mentors = Mentor.query.all()
        return render_template('mentor_reports.html', mentors=mentors)


@administrator.route('/student_csv', methods=['GET'])
@login_required
def student_csv():
    if request.method == 'GET':
        header = ['Student ID', 'Student Last Name', 'Student First Name', 'Student Address', 'Student Home Phone',
                  'Student Cell Phone', 'Student Email', 'Parent Email', 'Lunch Period', 'Time Registered',
                  'Graduation Year', 'Mentor ID', 'Opportunity Date', 'Opportunity Session', 'Mentor Name', 'Category',
                  'Description', 'Special Instructions', 'Contact Name', 'Buisness Phone', 'Buisness Email',
                  'Buisness Address']

        def generate():
            students = Student.query.filter_by(approved=True).all()
            if not students:
                return redirect(url_for('administrator.administrator_landing'))
            yield ','.join(header) + '\n'
            for student in students:
                opportunity = student.opportunity
                mentor = opportunity.mentor
                row = [student.id, student.last_name, student.first_name, student.address, student.home_phone,
                       student.cell_phone, student.student_email, student.parent_email, student.lunch_period,
                       student.registration_time, student.graduation_year, mentor.id, opportunity.date,
                       opportunity.session, mentor.mentor_name, mentor.category, mentor.description,
                       mentor.special_instructions, mentor.contact_name, mentor.phone, mentor.email, mentor.address]
                yield ','.join(map(str, row)) + '\n'

        return Response(generate(), mimetype='text/csv',
                        headers={'Content-Disposition': 'attachment; filename=students.csv'})


@administrator.route('/mentor_csv', methods=['GET'])
@login_required
def mentor_csv():
    if request.method == 'GET':
        header = ['Mentor ID', 'Mentor Name', 'Category', 'Contact Name', 'Description', 'Special Instructions',
                  'Address', 'Buisness Phone', 'Buisness Email', 'Status', 'Number of Opportunities',
                  'Total Students Registered', 'Opportunities:']

        def generate():
            mentors = Mentor.query.all()
            yield ','.join(header) + '\n'
            for mentor in mentors:
                opportunities = mentor.opportunities
                row = [mentor.id, mentor.mentor_name, mentor.category, mentor.contact_name, mentor.description,
                       mentor.special_instructions, mentor.address, mentor.phone, mentor.email,
                       format_status(mentor.status), len(opportunities)]
                opportunities_data = []
                total_students = 0
                for opportunity in opportunities:
                    total_students += len(opportunity.students)
                    opportunities_data.extend([format_date(opportunity.date), get_session(opportunity.session),
                                               '# Registered to Opportunity: ' + str(len(opportunity.students))])
                row.append(total_students)
                row.extend(opportunities_data)
                yield ','.join(map(str, row)) + '\n'

        return Response(generate(), mimetype='text/csv',
                        headers={'Content-Disposition': 'attachment; filename=mentors.csv'})


@administrator.route('/student_bulk', methods=['GET', 'POST'])
@login_required
def student_bulk():
    students = Student.query.filter_by(approved=True).all()
    if request.method == 'POST':
        error = ''
        try:
            bulk_message = get_message_from_form(request)
            include_schedule = True if request.form.get('include-schedule') else False
            send_copy_to_parents = True if request.form.get('parent') else False
            for student in students:
                schedule = ''
                if include_schedule:
                    schedule = get_schedule_from_student(student)
                recipients = [student.student_email]
                if send_copy_to_parents:
                    recipients.append(student.parent_email)
                message = Message(subject=bulk_message.subject, body=bulk_message.body + schedule,
                                  recipients=recipients)
                send_mail(message)
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                return render_template('student_bulk.html', error=error, students=students)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('student_bulk.html', students=students)


@administrator.route('/mentor_bulk', methods=['GET', 'POST'])
@login_required
def mentor_bulk():
    mentors = Mentor.query.all()
    registered_mentors = []
    for mentor in mentors:
        if has_registered_students(mentor):
            registered_mentors.append(mentor)
    if request.method == 'POST':
        error = ''
        try:
            bulk_message = get_message_from_form(request)
            registered_mentors_only = True if request.form.get('registered-mentors-only') else False
            include_registered_students = True if request.form.get('include-registered-students') else False
            if registered_mentors_only:
                for mentor in registered_mentors:
                    message = Message(bulk_message.subject, body=bulk_message.body, recipients=[mentor.email])
                    if include_registered_students:
                        message.html = get_schedule_from_mentor(mentor)
                    send_mail(message)
            else:
                for mentor in mentors:
                    message = Message(bulk_message.subject, body=bulk_message.body, recipients=[mentor.email])
                    send_mail(message)
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                return render_template('mentor_bulk.html', error=error, mentors=mentors,
                                       registered_mentors=registered_mentors)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('mentor_bulk.html', mentors=mentors, registered_mentors=registered_mentors)


@administrator.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    if request.method == 'POST':
        error = ''
        try:
            reset_system_from_form(request)
            remove_all_mentors = True if request.form.get('remove-mentors') else False
            remove_inactive_mentors = True if request.form.get('remove-inactive-mentors') else False
            mentors = Mentor.query.all()
            for mentor in mentors:
                for opportunity in mentor.opportunities:
                    db.session.delete(opportunity)
                for notification in mentor.notifications:
                    db.session.delete(notification)
            if remove_all_mentors:
                for mentor in mentors:
                    db.session.delete(mentor)
            if remove_inactive_mentors:
                for mentor in mentors:
                    if not mentor.status:
                        db.session.delete(mentor)
            db.session.commit()
        except UnconfirmedResetException:
            error = Errors.UNCONFIRMED_RESET_ERROR
        except InvalidResetOptionsException:
            error = Errors.INVALID_RESET_OPTIONS_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('reset.html', error=error)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('reset.html')
