import logging
import traceback
import os

from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from messages import Errors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.getenv('DATABASE_USERNAME', default='admin') + ':' + os.getenv('DATABASE_PASSWORD', default='password') + '@' + os.getenv('DATABASE_SERVER', default='localhost') + os.getenv('DATABASE_PORT', default='3306') + '/' + os.getenv('DATABASE_NAME')
app.secret_key = os.getenv('SECRET_KEY', default='8648d22e542ca1188d20de52b52c6d33d209704f508f21fc')
app.config['MAIL_SERVER'] = os.getenv('PROGRAM_EMAIL_SERVER')
app.config['MAIL_USERNAME'] = os.getenv('PROGRAM_EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.getenv('PROGRAM_EMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USER_SSL'] = False
app.config['MAIL_PORT'] = os.getenv('PROGRAM_EMAIL_PORT')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('PROGRAM_EMAIL_ADDRESS')

db = SQLAlchemy(app)
mail = Mail(app)

from helpers import *

login_manager = LoginManager()
login_manager.init_app(app)

from models import Administrator


@login_manager.user_loader
def load_user(user_id):
    return Administrator.query.get(user_id)


db.drop_all()
db.create_all()

from setup import setup

setup()

if __name__ == '__main__':
    app.run()


def send_mail(message):
    configuration = Configuration.query.first()
    if configuration.email:
        mail.send(message)


from mentor import mentor
from administrator import administrator
from student import student

app.register_blueprint(administrator)
app.register_blueprint(mentor)
app.register_blueprint(student)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        error = ''
        try:
            user = get_administrator_from_login(request)
            login_user(user)
        except IncompleteFormException:
            error = Errors.INCOMPLETE_FORM_ERROR
        except InvalidUsernameOrPasswordException:
            error = Errors.INVALID_USERNAME_OR_PASSWORD_ERROR
        except Exception as e:
            logging.exception(e)
            traceback.print_exc()
        finally:
            if error:
                return render_template('admin.html', error=str(error))
        return redirect(url_for('administrator.administrator_landing'))
    if request.method == 'GET':
        return render_template('admin.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin'))
