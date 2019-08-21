# Creates application object. File used as a starting point.

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mg_app_object = Flask(__name__)
mg_app_object.config.from_object(Config)
# Database object to represetn the database.
mg_db_object = SQLAlchemy(mg_app_object)
# Object to represent the migration engine.
migrate = Migrate(mg_app_object, mg_db_object)

# The bottom import here is a workaround to 'circular imports'
# models will define the structure of the database.
from mettle_and_grit_app_package import routes, models
