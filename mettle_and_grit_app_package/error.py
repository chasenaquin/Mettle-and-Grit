from flask import render_template
from mettle_and_grit_app_package import mg_app_object, mg_db_object

@mg_app_object.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@mg_app_object.errorhandler(500)
def internal_error(error):
    mg_db_object.session.rollback()
    return render_template('500.html'), 500
