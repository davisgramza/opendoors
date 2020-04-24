import datetime

from models import Opportunity


def is_complete_form(request, fields):
    for field in fields:
        if not request.form.get(field):
            return False
    return True


def is_valid_email(email):
    return '@' in email and '.' in email


def is_valid_status(status):
    return status == 'active' or status == 'inactive'


def is_valid_number_of_students(students):
    try:
        number = int(students)
        return number > 0
    except ValueError:
        return False


def is_valid_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_session(session):
    return session == 'am' or session == 'pm' or session == 'full'


def deletion_is_confirmed(confirmation):
    return confirmation == 'confirm'


def is_valid_program_status(status):
    return status == 'Active' or status == 'Preview' or status == 'Disabled'


def is_valid_email_notification_setting(email):
    return email == 'on' or email == 'off'


class NotificationIdentifiers:
    PROGRAM_ACTIVE = 'Program Active'
    PROGRAM_PREVIEW = 'Program Preview'
    PROGRAM_DISABLED = 'Program Disabled'
    DISCLAIMER = 'Disclaimer'
    SUBMISSION_TEXT = 'Submission Text'
    APPROVAL = 'Approval Email Text'
    DENIED = 'Denied Email Text'
    DELETED = 'Deleted Email Text'
    REGISTRATION_FIELDS = 'Mentor Registration Disclaimer'
    MENTOR_NOTIFICATION = 'Email Notification of Available Opportunity For Mentor'


def is_valid_opportunity(mentor, opportunity_id):
    try:
        opportunity_id = int(opportunity_id)
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity or opportunity.mentor != mentor:
            return False
        if len(opportunity.students) >= mentor.students:
            return False
        return True
    except ValueError:
        return False


def mentor_fully_registered(mentor):
    students = mentor.students
    for opportunity in mentor.opportunities:
        if len(opportunity.students) < students:
            return False
    return True


def confirmation_is_confirmed(request):
    if request.form.get('confirmation') != 'confirm':
        return False
    return True


def has_registered_students(mentor):
    for opportunity in mentor.opportunities:
        if len(opportunity.students) > 0:
            return True
    return False
