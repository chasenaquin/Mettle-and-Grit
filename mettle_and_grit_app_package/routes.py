# routes module represents the different URLs that the application implements.
# Handlers for the application routes are called view functions.
# View functions are mapped to one or more route URLs.

from mettle_and_grit_app_package import mg_app_object, mg_db_object
from mettle_and_grit_app_package.models import User
from mettle_and_grit_app_package.forms import LoginForm, RegistrationForm, EditProfileForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@mg_app_object.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        mg_db_object.session.commit()

@mg_app_object.route('/')
# @app.route is known as a decorator.File
# A decorator modifies the function that follows it.

@mg_app_object.route('/index')
# REquires a user to be logged in to see content
@login_required
def index():
    #Mock user dictionary
#  user = {'username':'Mr. Chase Naquin'}
    # Render_template takes a template filename and a wariable list of template
    # arguments and returns the same template, but with all the placeholders
    # in it replaced with actual values using Jinja2 template engine
    # substitutions using the {{...}} blocks.
    return render_template('index.html', title='Home')
#def protected_page():
#    return Render_template('protected_page', title='PP', user=user)

@mg_app_object.route('/login', methods=['GET', 'POST'])
def login():
    # Handels if a currently authenticated user navigates to login page.
    # Current_user can be used at any time during the handling. The user object
    # can be a user id from the database or a special anonymous user object.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Establishing method for Sign Im button to work allowing POST requests to
    # be accepted and processed. The 'form.validate_on_submit' method does
    # all of the form processing work. When the browser sned the GET request
    # to receive teh web page with the form, this method is going to return
    # FALSE, so in tht case the function skipe the if statement and goes
    # directly to render the template in the last line of the function. When
    # 'form.validate_on_submit()' returns TRUE, the login view function calls
    # two functions. The 'Flash' function is a uesful way to show the user
    # something. For example, if something was successful or not. The 'redirect'
    # function instructs the web client web browser to automatically navigate
    # to a different page, given as an argument.
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Uses Flask-Login and will resigster the user as logged in and
        # current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)
        # Right after the user is logged in by calling login-user() function, the
        # value of next query string argument is obtained.
        # The request variable contains all that information that the client
        # sent with the request
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # The form=form is passing the form object created above to the template
    # with the name form.
    return render_template('login.html', title="Sign In", form=form)

@mg_app_object.route('/logout')
def logout():
    logout_user()
    # arguments and returns the same template, but with all the placeholders
    # in it replaced with ac
    return redirect(url_for('index'))

@mg_app_object.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        mg_db_object.session.add(user)
        mg_db_object.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Using a dynamic url component <username>
# When a route has a dynamic component, Flask will accept any test in that portion of
# th URL, and will invoke the view function with the actual text argument.
@mg_app_object.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@mg_app_object.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.status = form.status.data
        mg_db_object.session.commit()
#        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.status.data = current_user.status
    return render_template('edit_profile.html', title='Edit Profile',form=form)
