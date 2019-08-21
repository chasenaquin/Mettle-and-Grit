# Defines the Flask application instance.

from mettle_and_grit_app_package import mg_app_object
from mettle_and_grit_app_package.models import User

@mg_app_object.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User}
