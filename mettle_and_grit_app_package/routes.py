# routes module represents the different URLs that the application implements.
# Handlers for the application routes are called view functions.
# View functions are mapped to one or more route URLs.

from mettle_and_grit_app_package import mg_app_object
from flask import render_template, flash, redirect
from mettle_and_grit_app_package.forms import LoginForm

@mg_app_object.route('/')
# @app.route is known as a decorator.
# A decorator modifies the function that follows it.

@mg_app_object.route('/index')
def index():
    #Mock user dictionary
    user = {'username':'Mr. Chase Naquin'}
    # Render_template takes a template filename and a wariable list of template
    # arguments and returns the same template, but with all the placeholders
    # in it replaced with actual values using Jinja2 template engine
    # substitutions using the {{...}} blocks.
    return render_template('index.html', title='Mettle and Grit', user=user)

@mg_app_object.route('/login', methods=['GET', 'POST'])
def login():
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
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    # The form=form is passing the form object created above to the template
    # with the name form.
    return render_template('login.html', title="Sign In", form=form)
