# app/__init__.py

# third-party imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import os
from . import views
from . import database
import json
#import models

# local imports
import config as cfg

# db variable initialization
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../resources.db"))
db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        return json.dumps(user_dict)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'username', 'email')
        model = User
        sqla_session = db.session

user_schema = UserSchema()
users_schema = UserSchema(many=True)
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        new_user = User(
            username=request.json['username'],
            email=request.json['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)

    def delete(self):
        User.query.delete()
        db.session.commit()
        return '', 204

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def patch(self, user_id):
        user = User.get_or_404(user_id)

        if 'username' in request.json:
            user.username = request.json['user']
        if 'email' in request.json:
            user.email = request.json['email']
        
        db.session.commit()
        return user_schema.dump(user)
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(cfg.app_config['development'])
    #app.register_blueprint(views.bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    #from . import database
    #database.init_db()
    api = Api(app)
    ma.init_app(app)
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/user/<int:user_id>')
    @app.route('/')
    @app.route('/home')
    def home_page():
        #models.test_db()
        return render_template('home.html')

    @app.route('/users_page')
    def users_page():
        #models.test_db()
        users = User.query.all()
        print(users)
        for user in users:
            print(user.username)
            print(user.email)
        return render_template('users.html', users=users)
    #db.init_app(app)

    #@app.teardown_appcontext
    #def shutdown_session(exception=None):
    #    database.db_session.remove()

    return app
