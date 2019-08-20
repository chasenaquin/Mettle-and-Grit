from flask import Flask
from config import Config

mg_app_object = Flask(__name__)
mg_app_object.config.from_object(Config)

from mettle_and_grit_app_package import routes
