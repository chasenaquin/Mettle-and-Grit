from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from mettle_and_grit_app_package.models import User

class LoginForm(FlaskForm):
    # For each field, and object is created as a class variable in the LoginForm
    # class. Each field is given a description/lable as the first argument.
    # The optional/additional validator 'DataRequired' simply checks if empty.
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # Email validator comes stock in WTForms to ensure input matches the structure of an email address.
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # EqualTo is a stock validator in WTForms to ensure value is identical to specified field.
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # The validate_<FieldName> method causes WTForms to invoke them in addition to the stock validators
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already registered. Please select a different username')

    def validate_email(self, email):
        email=User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email is already registered. Please enter a different email address')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    status = TextAreaField('Status', validators=[Length(min=0, max=300)])
    submit = SubmitField('Submit')

    # Fixing the edit profile edit username to a username that is already in use.
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username is already in use. Please choose a different username.')
