# app/__init__.py

# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from . import views

# local imports
import config as cfg

# db variable initialization
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../resources.db"))

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(cfg.app_config['development'])
    app.register_blueprint(views.bp)
    #db = SQLAlchemy(app)
    from . import database
    database.init_db()
    #db.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.db_session.remove()

    return app
