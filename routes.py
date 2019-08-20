from mettle_and_grit_app_package import mg_app_object
from flask import render_template

@mg_app_object.route('/')
@mg_app_object.route('/index')
def index():
    user = {'username': 'Mr. Naquin'}
    return render_template('index.html', title='Home', user=user)

@mg_app_object.route('/home')
def home():
    return render_template('index.html', title='Home', user=user)

@mg_app_object.route('/articles')
def articles():
    return render_template('atricles.html', title='articles', user=user)

@mg_app_object.route('/calculators')
def calculators():
    return render_template('calculators.html', title='calculators', user=user)

@mg_app_object.route('/generators')
def generators():
    return render_template('generators.html', title='generators', user=user)

@mg_app_object.route('/profile')
def profile():
    return render_template('profile.html', title='profile', user=user)

@mg_app_object.route('/search')
def search():
    return render_template('search.html', title='search', user=user)

@mg_app_object.route('/login')
def login():
    return render_template('login.html', title='login', user=user)
