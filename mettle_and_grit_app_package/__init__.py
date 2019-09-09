# Creates application object. File used as a starting point.

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

mg_app_object = Flask(__name__)
mg_app_object.config.from_object(Config)
# Database object to represetn the database.
mg_db_object = SQLAlchemy(mg_app_object)
# Object to represent the migration engine.
migrate = Migrate(mg_app_object, mg_db_object)
# Creates and initializes Flask-Login
login = LoginManager(mg_app_object)
# Flask-Login forces users to authenticate before they can access certain content
# Flask-Login will redirect user to login form, and only redirect back once the
# login process is complete. The login value is the login view (routes).
login.login_view='login'

# Runs the email logger when debug mode is DISABLED.
if not mg_app_object.debug:
    if mg_app_object.config['MAIL_SERVER']:
        auth = None
        if mg_app_object.config['MAIL_USERNAME'] or mg_app_object.config['MAIL_PASSWORD']:
            auth = (mg_app_object.config['MAIL_USERNAME'], mg_app_object.config['MAIL_PASSWORD'])
        secure = None
        if mg_app_object.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(mg_app_object.config['MAIL_SERVER'], mg_app_object.config['MAIL_PORT']),
            fromaddr='no-reply@' + mg_app_object.config['MAIL_SERVER'],
            toaddrs=mg_app_object.config['ADMINS'], subject='M&G Production Failure Notification Email',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        mg_app_object.logger.addHandler(mail_handler)

# Enabling File Logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/Mettle_and_Grit_Production.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    mg_app_object.logger.addHandler(file_handler)

    mg_app_object.logger.setLevel(logging.INFO)
    mg_app_object.logger.info('-----===[ Mettle And Grit Flask Application Startup ]===-----')

# The bottom import here is a workaround to 'circular imports'
# models will define the structure of the database.
from mettle_and_grit_app_package import routes, models, error
