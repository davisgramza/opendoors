class IncompleteFormException(Exception):
    pass


class InvalidUsernameOrPasswordException(Exception):
    pass


class InvalidEmailException(Exception):
    pass


class InvalidStatusException(Exception):
    pass


class InvalidNumberOfStudentsException(Exception):
    pass


class InvalidOpportunityDateException(Exception):
    pass


class InvalidOpportunitySessionException(Exception):
    pass


class NoOpportunityException(Exception):
    pass


class UnconfirmedDeletionException(Exception):
    pass


class InvalidProgramStatusException(Exception):
    pass


class InvalidEmailNotificationSettingException(Exception):
    pass


class InvalidSelectedOpportunityException(Exception):
    pass


class StudentConfirmationUnconfirmedException(Exception):
    pass


class UnconfirmedResetException(Exception):
    pass


class InvalidResetOptionsException(Exception):
    pass


class MentorHasRegisteredStudentsException(Exception):
    pass


class DuplicateEmailException(Exception):
    pass
