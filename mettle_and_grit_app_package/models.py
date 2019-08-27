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
from mettle_and_grit_app_package import mg_db_object, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# Building out User Table. Class inherits from .Model.
# Usermixin indludes generic implementations like "is_authenticated",
# "is_active", "is_ananymous", an "get_id".
class User(UserMixin, mg_db_object.Model):
    # Fields are created as instances of the db.Column class.
    id = mg_db_object.Column(mg_db_object.Integer, primary_key=True)
    username = mg_db_object.Column(mg_db_object.String(64), index=True, unique=True)
    email = mg_db_object.Column(mg_db_object.String(120), index=True, unique=True)
    #Security best practices to NOT store plain text passwords.
    password_hash = mg_db_object.Column(mg_db_object.String(128))

    # NOTICE: There is an incosistenct that in some cases such as db.relationship()
    # call, the model is referenced by the model class, but in the db.ForeignKey()
    # declaration, a model is given by its database table name.

    # This db.relationship() is not actually a db field, but a high level overview
    # of the relationship between user and posts. For a One-to-Many relationship
    # the db.relationship is usually defined on 1 side and is a convinient way to
    # get access to the many. The first argument is the model class that represents
    # the many. The 'backref' argument defines the name of the field that will
    # be added to the objects of the "many" class that points back to the one object.
    # The lazy argument defines how the db query for the relationship will work.

#      posts = mg_db_object.relationship('Post', backref='author', lazy='dynamic')

    # This tells python how to print objects of this class.
    # returns "self" from the db
    # NEED TO FIND OUT HOW THIS WORKS
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lowe().encode('utf')).hexdigest()
        retuen 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

# Flask-Login keeps track of the logged in user by storing its unique indentifier
# in Flask's 'user session' which is a storage space assigned to each user who
# connects to the application. Each time the logged-in user navigates to a new
# page, Flask-Login retrieves the ID of that user from the session and then
# loads it into memory.
# Flask-Login knows nothing about databases, so it needs the applications help
# in loading the user. The extension expects that the application will configure
# a user loader function, that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#################
# Example "Post" Class and DB Model.
#class Post(db.Model):
#    id = mg_db_object.Column(db.Integer, primary_key=True)
#    body = mg_db_object.Column(db.String(140))
    # When you pass a function as a default, SQLAlchemy will set the field to the
    # value of calling that function. The datetime.utc now is passing the function itself
    # and not the result of calling it.
#    timestamp = mg_db_object.Column(mg_db_object.DateTime, index=True, default=datetime.utcnow)
    # user_id field is set to ForeignKey. It references the id field in the users table.
#    user_id = mg_db_object.Column(mg_db_object.Integer, db.ForeignKey('user.id'))

#    def __repr__(self):
#        return '<Post {}>'.format(self.body)
##################
