# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# local imports
from config import app_config
#from models import User

# db variable initialization
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../resources.db"))
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    from app import models

    @app.route('/')
    @app.route('/home')
    def home_page():
        #models.test_db()
        print(models.User.query.all())
        return "Home Page"

    return app