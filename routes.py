class AdministratorLogin:
    FIELDS = ['username', 'password']


class AddMentor:
    FIELDS = ['mentor-name', 'category', 'description', 'special-instructions', 'contact-name', 'students', 'phone',
              'email', 'address', 'status']


class EditMentor:
    FIELDS = ['mentor-name', 'category', 'description', 'special-instructions', 'contact-name', 'students', 'phone',
              'email', 'address', 'status']


class DeleteMentor:
    FIELDS = ['confirmation']


class EditConfiguration:
    FIELDS = ['program-status', 'email']


class Register:
    FIELDS = ['last-name', 'first-name', 'address', 'home-phone', 'cell-phone', 'student-email', 'parent-email',
              'lunch-period', 'graduation-year', 'opportunity', 'terms']


class DeleteStudent:
    FIELDS = ['confirmation']


class ConfirmStudent:
    FIELDS = ['confirmation']


class BulkEmails:
    FIELDS = ['subject', 'message']


class Reset:
    FIELDS = ['confirmation']


class GetNotifications:
    FIELDS = ['email']
