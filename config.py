# Separation of concerns = keep configuration options/variables in separate
# file. Use a class to store configuration variables.
# Configuration settings are defined as a class variable inside the Config
# class.
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SECRET_KEY - Flask and some of its extensions use the value of this
    #secret key as a cryptogrphic key useful to generate signatures or tokens.
    #Flask-WTF uses this to protect against Cross-Site Request Forgery (CSRF).
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLAlchemy extension takes the location of the application's database from
    # the SQLALCHEMY_DATABASE_URI confiuration variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mg_app.db')
    # Set to NOT signal the application everytime a change is made in the db.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
