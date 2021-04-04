# app/__init__.py

# third-party imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import os
import json

# local imports
import config as cfg

# db variable initialization
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../resources.db"))
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(cfg.app_config['development'])

    from . import views
    app.register_blueprint(views.bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    ma.init_app(app)

    api.add_resource(views.UserListResource, '/users')
    api.add_resource(views.UserResource, '/user/<int:user_id>')
    api.add_resource(views.ResourceListResource, '/resources')

    return app
