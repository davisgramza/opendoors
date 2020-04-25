import logging
import traceback

from flask import request, render_template, redirect, Blueprint, url_for
from flask_login import current_user, login_required

from app import db
from helpers import *
from messages import Errors

mentor = Blueprint('mentor', __name__, template_folder='templates')


@mentor.route('/add_mentor', methods=['GET', 'POST'])
@login_required
def add_mentor():
    if request.method == 'POST':
        error = ''
        try:
            added_mentor = get_mentor_from_form(request)
            opportunities = get_opportunities_from_form(request, added_mentor)
            db.session.add(added_mentor)
            for opportunity in opportunities:
                db.session.add(opportunity)
            db.session.commit()
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except InvalidEmailException:
            error = Errors.INVALID_EMAIL_ERROR
        except InvalidStatusException:
            error = Errors.INVALID_STATUS_ERROR
        except InvalidNumberOfStudentsException:
            error = Errors.INVALID_NUMBER_OF_STUDENTS_ERROR
        except InvalidOpportunityDateException:
            error = Errors.INVALID_OPPORTUNITY_DATE_ERROR
        except InvalidOpportunitySessionException:
            error = Errors.INVALID_OPPORTUNITY_SESSION_ERROR
        except NoOpportunityException:
            error = Errors.NO_OPPORTUNITIES_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('add_mentor.html', error=error)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('add_mentor.html')


@mentor.route('/edit_mentor/<mid>', methods=['GET', 'POST'])
@login_required
def edit_mentor(mid):
    edited_mentor = Mentor.query.get(mid)
    has_students = has_registered_students(edited_mentor)
    if not edited_mentor:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'POST':
        error = ''
        try:
            edit_mentor_from_form(request, edited_mentor)
            opportunities = edit_opportunities_from_form(request, edited_mentor)
            for opportunity in opportunities.get('add'):
                db.session.add(opportunity)
            for opportunity in opportunities.get('delete'):
                db.session.delete(opportunity)
            db.session.commit()
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except InvalidEmailException:
            error = Errors.INVALID_EMAIL_ERROR
        except InvalidStatusException:
            error = Errors.INVALID_STATUS_ERROR
        except InvalidNumberOfStudentsException:
            error = Errors.INVALID_NUMBER_OF_STUDENTS_ERROR
        except InvalidOpportunityDateException:
            error = Errors.INVALID_OPPORTUNITY_DATE_ERROR
        except InvalidOpportunitySessionException:
            error = Errors.INVALID_OPPORTUNITY_SESSION_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('edit_mentor.html', mentor=edited_mentor, error=error, has_students=has_students)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('edit_mentor.html', mentor=edited_mentor, has_students=has_students)


@mentor.route('/delete_mentor/<mid>', methods=['GET', 'POST'])
@login_required
def delete_mentor(mid):
    deleted_mentor = Mentor.query.get(mid)
    if not deleted_mentor:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'POST':
        error = ''
        try:
            delete_mentor_from_form(request, deleted_mentor)
            db.session.delete(deleted_mentor)
            db.session.commit()
        except UnconfirmedDeletionException:
            error = Errors.UNCONFIRMED_DELETION_ERRROR
        except MentorHasRegisteredStudentsException:
            error = Errors.MENTOR_HAS_REGISTERED_STUDENTS_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                db.session.rollback()
                return render_template('delete_mentor.html', error=error, mentor=deleted_mentor)
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('delete_mentor.html', mentor=deleted_mentor,
                               registered=has_registered_students(deleted_mentor))


@mentor.route('/view_mentors', methods=['GET'])
@login_required
def view_mentors():
    configuration = Configuration.query.first()
    if request.method == 'GET':
        if request.args.get('search'):
            query = '%' + request.args.get('search') + '%'
            mentors = Mentor.query.filter(
                Mentor.mentor_name.like(query) | Mentor.description.like(query) | Mentor.category.like(query)).all()
        else:
            mentors = Mentor.query.all()
        if current_user.is_authenticated:
            return render_template('view_mentors.html', mentors=mentors, admin=True, get_session=get_session,
                                   format_date=format_date, status=configuration.program_status)
        else:
            if configuration.program_status != 'Active':
                return redirect(url_for('student.landing'))
            return render_template('view_mentors.html', mentors=mentors, get_session=get_session,
                                   format_date=format_date, status=configuration.program_status)


@mentor.route('/view_mentor/<mid>', methods=['GET'])
@login_required
def view_mentor(mid):
    queried_mentor = Mentor.query.get(mid)
    if not queried_mentor:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('view_mentor.html', mentor=queried_mentor)


@mentor.route('/mentor_schedule/<mid>', methods=['GET'])
@login_required
def mentor_schedule(mid):
    scheduled_mentor = Mentor.query.get(mid)
    if not scheduled_mentor:
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('mentor_schedule.html', mentor=scheduled_mentor, get_session=get_session,
                               format_date=format_date)
