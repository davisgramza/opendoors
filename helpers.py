from flask_mail import Message
from werkzeug.security import check_password_hash

from exceptions import *
from models import *
from routes import *
from validations import *


def get_administrator_from_login(request):
    if not is_complete_form(request, AdministratorLogin.FIELDS):
        raise IncompleteFormException()
    user = Administrator.query.filter_by(username=request.form.get('username')).first()
    if not user or not check_password_hash(user.hash, request.form.get('password')):
        raise InvalidUsernameOrPasswordException()
    return user


def get_amount_of_students(students):
    return int(students)


def get_status(status):
    return status == 'active'


def format_status(status):
    if status:
        return 'Active'
    else:
        return 'Inactive'


def format_date(date):
    information = datetime.datetime.strptime(date, '%Y-%m-%d')
    return str(information.month) + '/' + str(information.day) + '/' + str(information.year)


def get_date(date):
    information = datetime.datetime.strptime(date, '%m/%d/%Y')
    return str(information.year) + '-' + str(information.month) + '-' + str(information.day)


def get_email_notification_setting(email):
    return email == 'on'


def validate_mentor(request, fields):
    if not is_complete_form(request, fields):
        raise IncompleteFormException()
    if not is_valid_email(request.form.get('email')):
        raise InvalidEmailException()
    if not is_valid_status(request.form.get('status')):
        raise InvalidStatusException()
    if not is_valid_number_of_students(request.form.get('students')):
        raise InvalidNumberOfStudentsException()


def get_mentor_from_form(request):
    validate_mentor(request, AddMentor.FIELDS)
    return Mentor(mentor_name=request.form.get('mentor-name'), category=request.form.get('category'),
                  description=request.form.get('description'),
                  special_instructions=request.form.get('special-instructions'),
                  contact_name=request.form.get('contact-name'), phone=request.form.get('phone'),
                  email=request.form.get('email'), address=request.form.get('address'),
                  students=get_amount_of_students(request.form.get('students')),
                  status=get_status(request.form.get('status')))


def get_opportunity_number(opportunity):
    number = ''
    for character in opportunity:
        if character.isdigit():
            number += character
    if number:
        return int(number)
    else:
        return None


def get_opportunities_numbers(request):
    numbers = set()
    for opportunity in request.form.keys():
        number = get_opportunity_number(opportunity)
        if number:
            numbers.add(number)
    return numbers


def get_opportunities_from_form(request, mentor):
    opportunities = []
    numbers = list(get_opportunities_numbers(request))
    if not numbers:
        raise NoOpportunityException()
    for number in numbers:
        date = request.form.get('opportunity' + str(number) + 'date')
        session = request.form.get('opportunity' + str(number) + 'session')
        if not date and not session:
            continue
        if not date or not session:
            raise IncompleteFormException()
        if not is_valid_date(date):
            raise InvalidOpportunityDateException()
        if not is_valid_session(session):
            raise InvalidOpportunitySessionException()
        opportunity = Opportunity(date=get_date(date), session=session, mentor=mentor)
        opportunities.append(opportunity)
    return opportunities


def edit_mentor_from_form(request, mentor):
    validate_mentor(request, EditMentor.FIELDS)
    mentor.mentor_name = request.form.get('mentor-name')
    mentor.category = request.form.get('category')
    mentor.description = request.form.get('description')
    mentor.special_instructions = request.form.get('special-instructions')
    mentor.contact_name = request.form.get('contact-name')
    mentor.phone = request.form.get('phone')
    mentor.email = request.form.get('email')
    mentor.address = request.form.get('address')
    if not has_registered_students(mentor):
        mentor.students = get_amount_of_students(request.form.get('students'))
    mentor.status = get_status(request.form.get('status'))


def edit_opportunities_from_form(request, mentor):
    changes = {'add': [], 'delete': []}
    current_index = len(mentor.opportunities)
    numbers = list(get_opportunities_numbers(request))
    for number in range(1, current_index + 1):
        date = request.form.get('opportunity' + str(number) + 'date')
        session = request.form.get('opportunity' + str(number) + 'session')
        if not date and not session:
            changes.get('delete').append(mentor.opportunities[number - 1])
            continue
        if not date or not session:
            raise IncompleteFormException()
        if not is_valid_date(date):
            raise InvalidOpportunityDateException()
        if not is_valid_session(session):
            raise InvalidOpportunitySessionException()
        opportunity = mentor.opportunities[number - 1]
        if not opportunity.students:
            opportunity.date = date
            opportunity.session = session
    for number in numbers:
        date = request.form.get('opportunity' + str(number) + 'date')
        session = request.form.get('opportunity' + str(number) + 'session')
        if number <= current_index:
            continue
        if not date and not session:
            continue
        if not date or not session:
            raise IncompleteFormException()
        if not is_valid_date(date):
            raise InvalidOpportunityDateException()
        if not is_valid_session(session):
            raise InvalidOpportunitySessionException()
        changes.get('add').append(Opportunity(date=date, session=session, mentor=mentor))
    return changes


def delete_mentor_from_form(request, mentor):
    if not is_complete_form(request, DeleteMentor.FIELDS) or not deletion_is_confirmed(
            (request.form.get('confirmation'))):
        raise UnconfirmedDeletionException()
    if has_registered_students(mentor):
        raise MentorHasRegisteredStudentsException()


def edit_configuration_from_form(request, configuration):
    if not is_complete_form(request, EditConfiguration.FIELDS):
        raise IncompleteFormException()
    if not is_valid_program_status(request.form.get('program-status')):
        raise InvalidProgramStatusException()
    if not is_valid_email_notification_setting(request.form.get('email')):
        raise InvalidEmailNotificationSettingException()
    configuration.program_status = request.form.get('program-status')
    configuration.email = get_email_notification_setting(request.form.get('email'))


def edit_notifications_from_form(request, notifications):
    fields = []
    for notification in notifications:
        fields.append(str(notification.id))
    if not is_complete_form(request, fields):
        raise IncompleteFormException()
    for notification in notifications:
        notification.message = request.form.get(str(notification.id))


def get_status_from_configuration(configuration):
    if configuration == 'Active':
        return NotificationIdentifiers.PROGRAM_ACTIVE
    elif configuration == 'Preview':
        return NotificationIdentifiers.PROGRAM_PREVIEW
    else:
        return NotificationIdentifiers.PROGRAM_DISABLED


def get_session(session):
    if session == 'am':
        return 'A.M. Session'
    elif session == 'pm':
        return 'P.M. Session'
    elif session == 'full':
        return 'Full Day Session'
    else:
        return


def get_registered_opportunity_from_form(opportunity_id):
    return Opportunity.query.get(int(opportunity_id))


def get_student_from_form(request, mentor):
    if not is_complete_form(request, Register.FIELDS):
        raise IncompleteFormException()
    if not is_valid_email(request.form.get('student-email')) or not is_valid_email(request.form.get('parent-email')):
        raise InvalidEmailException()
    if not is_valid_opportunity(mentor, request.form.get('opportunity')):
        raise InvalidSelectedOpportunityException()
    return Student(last_name=request.form.get('last-name'), first_name=request.form.get('first-name'),
                   address=request.form.get('address'), home_phone=request.form.get('home-phone'),
                   cell_phone=request.form.get('cell-phone'), student_email=request.form.get('student-email'),
                   parent_email=request.form.get('parent-email'), lunch_period=request.form.get('lunch-period'),
                   graduation_year=request.form.get('graduation-year'),
                   opportunity=get_registered_opportunity_from_form(request.form.get('opportunity')))


def delete_student_from_form(request):
    if not is_complete_form(request, DeleteStudent.FIELDS) or not deletion_is_confirmed(
            (request.form.get('confirmation'))):
        raise UnconfirmedDeletionException()


def confirm_student_from_form(request):
    if not is_complete_form(request, ConfirmStudent.FIELDS) or not confirmation_is_confirmed(request):
        raise StudentConfirmationUnconfirmedException


def get_confirmed_students_from_form(request):
    students = []
    for field in request.form.keys():
        try:
            student = Student.query.get(int(field))
            if request.form.get(field) == 'confirm' and student:
                students.append(student)
        except ValueError:
            continue
    return students


def get_message_from_form(request):
    if not is_complete_form(request, BulkEmails.FIELDS):
        raise IncompleteFormException()
    return Message(request.form.get('subject'), body=request.form.get('message'))


def get_schedule_from_student(student):
    return '\nYour shadowing opportunity will take place on ' + format_date(
        student.opportunity.date) + ' during the ' + get_session(
        student.opportunity.session) + '.\n' + 'Your opportunity with ' + student.opportunity.mentor.mentor_name + ' will take place at ' + student.opportunity.mentor.address + '.\n' + 'Special Instructions: ' + student.opportunity.mentor.special_instructions


def reset_system_from_form(request):
    if not is_complete_form(request, DeleteStudent.FIELDS) or not deletion_is_confirmed(
            (request.form.get('confirmation'))):
        raise UnconfirmedResetException()
    if request.form.get('remove-mentors') and request.form.get('remove-inactive-mentors'):
        raise InvalidResetOptionsException()


def get_mentor_notification_from_form(request, mentor):
    if not is_complete_form(request, GetNotifications.FIELDS):
        raise IncompleteFormException()
    if not is_valid_email(request):
        raise InvalidEmailException()
    notifications = MentorNotification.query.filter(email=request.form.get('email'), mentor=mentor).all()
    if notifications:
        raise DuplicateEmailException()
    return MentorNotification(email=request.form.get('email'), mentor=mentor)


def get_schedule_from_mentor(mentor):
    html = '''
    <table>
        <th colspan="2">
            <th>Registered Students</th>
        <th>
    '''
    i = 0
    for opportunity in mentor.opportunities:
        i += 1
        html += '''
            <tr>
                <td style="border-top: 1px solid black;">Opportunity #{}.</td>
                <td style="border-top: 1px solid black;">{}</td>
            </tr>
            <tr>
                <td>Session Type:</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Registered Students:</td>
                <td>
                
        '''.format(i, format_date(opportunity.date), get_session(opportunity.session))
        if opportunity.students:
            for student in opportunity.students:
                html += '''
                    <div style="border: 1px solid black; padding: 3px">
                        <p>Name: {} {}</p>
                        <p>Address: {}</p>
                        <p>Home Phone: {}</p>
                        <p>Cell Phone: {}</p>
                        <p>Student Email: {}</p>
                        <p>Parent Email: {}</p>
                        <p>Lunch Period: {}</p>
                        <p>Graduation Year: {}</p>
                    </div>
                '''.format(student.first_name, student.last_name, student.address, student.home_phone,
                           student.cell_phone, student.student_email, student.parent_email, student.lunch_period,
                           student.graduation_year)
        else:
            html += 'No Registered Students'
        html += '</td></tr>'
    html += '</table>'
    return html
