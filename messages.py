class Errors:
    INCOMPLETE_FORM_ERROR = 'The form was not fully completed. Please fully complete the form.'
    INVALID_USERNAME_OR_PASSWORD_ERROR = 'The username or password was incorrect.'
    INVALID_EMAIL_ERROR = 'The entered email was invalid'
    INVALID_NUMBER_OF_STUDENTS_ERROR = 'The entered number of students was invalid. It must be an integer greater ' \
                                       'than zero. '
    INVALID_STATUS_ERROR = 'The enterd status was invalid. Must be active or inactive.'
    INVALID_OPPORTUNITY_DATE_ERROR = 'The opportunity date was invalid.'
    INVALID_OPPORTUNITY_SESSION_ERROR = 'The opportunity session selected was invalid.'
    NO_OPPORTUNITIES_ERROR = 'You must have at least one opportunity for a mentor'
    UNCONFIRMED_DELETION_ERRROR = 'The deletion was unconfirmed.'
    INVALID_PROGRAM_STATUS_ERROR = 'The program status is invalid. Please choose between Active/Preview/Disabled'
    INVALID_EMAIL_NOTIFICATION_SETTING_ERROR = 'The email notification setting is invalid. Please choose between On/Off'
    INVALID_SELECTED_OPPORTUNITY_ERROR = 'The opportunity selected is either full or not available. Please choose another opportunity.'
    STUDENT_CONFIRMATION_UNCONFIRMED_ERROR = 'The confirmation was not confirmed.'
    UNCONFIRMED_RESET_ERROR = 'To reset the system with the selected options, you must confirm that you want to reset the program.'
    INVALID_RESET_OPTIONS_ERROR = 'You may not select both remove inactive mentors and remove all mentors. You may select only one.'
    MENTOR_HAS_REGISTERED_STUDENTS_ERROR = 'This mentor can not be deleted as it already has registered students.'
    DUPLICATE_EMAIL_ERROR = 'You can not register for more than one notification reminder per email.'


class Successes:
    MENTOR_NOTIFICATION_REGISTRATION_SUCCESS = 'You have successfully registered for email reminders that will notifiy you if an opportunity with the selected mentor becomes available. Please check your email periodically as available opportunities come on a first come, first serve basis.'
