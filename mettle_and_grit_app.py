# Defines the Flask application instance.

from mettle_and_grit_app_package import mg_app_object
from mettle_and_grit_app_package.models import User

#Used for Flash Shell Pre-Loading.
@mg_app_object.shell_context_processor
def make_shell_context():
#   return {'db' : mg_app_object, 'User': User, 'Post': Post}
    return {'db': mg_app_object, 'User': User}
