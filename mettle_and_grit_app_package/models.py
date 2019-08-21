# The data that will be stored in the database will be represented by a
# collection of classes called database models. The ORM layer within SQLAlchemy
# will do the translations required to map objects from these classes into rows
# in proper dtabase tables.

# On initial db creation, you will need to use flask db init, set the FLASK_APP
# variable, and issue a flask db migrate -m "table name", flask db upgrade to
# make changes. Will have to create database in MySQL before running 'upgrade'

# SQLAlchemy uses "snake case". "Users" model below will be "users" in db.
# "AddressAndPhone" would be "address_and_phone". You can specify table names
# be adding an attribute names "__tablename__" to the model class.

#See more details on usages and best practices for "flask-migrate"
from mettle_and_grit_app_package import mg_db_object
from datetime import datetime

# Building out User Table. Class inherits from Model.
class User(mg_db_object.Model):
    # Fields are created as instances of the db.Column class.
    id = mg_db_object.Column(mg_db_object.Integer, primary_key=True)
    username = mg_db_object.Column(mg_db_object.String(64), index=True, unique=True)
    email = mg_db_object.Column(mg_db_object.String(120), index=True, unique=True)
    #Security best practices to NOT store plain text passwords.
    password_hash = mg_db_object.Column(mg_db_object.String(128))
    #created_at = mg_db_object.Column(mg_db_object.DateTime, index=True, default=datetime.utcnow)
    #For Different Table using Foreign Key: user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Add to users tp creat that db.relationship. db.relationship uses the Class
    # compared to the table name as in the ForeignKey declaration.
    #posts = db.relationship('Post', backref='author', lazy='dynamic')

    # This tells python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Reference: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
