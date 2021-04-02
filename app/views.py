import functools
from flask import Blueprint, render_template, jsonify, request, url_for
from flask_restful import Api, Resource
from . import models
from app import db
from . import database
import json

bp = Blueprint('files', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/home')
def home_page():
    #models.test_db()
    return render_template('home.html')

@bp.route('/users_page')
def users_page():
    #models.test_db()
    users = models.User.query.all()
    print(users)
    for user in users:
        print(user.username)
        print(user.email)
    return render_template('users.html', users=users)

"""
@bp.route('/users', methods=['GET', 'POST'])
def users_data():
    users = models.User.query.all()
    if request.method == 'POST':
        a_user = json.loads(request.data)
        print(a_user)
        print(request.json)
        print(request.json.email)
        user = models.User(email=request.json.email,
                    username=request.json.username)
        new_user = schema.load(user, session=db.session).data
        users.append(user)
        database.db_session.add(user)
        database.db_session.commit()
        flash('You have successfully registered!')
        return redirect(url_for('users_page'))
    print(users)
    return f'{users}'

@bp.route('/user/:{user}', methods=['GET', 'POST'])
def user_data():
    users = models.User.query.all()
    if request.method == 'POST':
        users.append(request.users)
        return redirect(url_for('users_page'))
    print(users)
    return f'{users}'
"""

class UserListResource(Resource):
    def get(self):
        users = models.User.query.all()
        return models.users_schema.dump(users)

    def post(self):
        new_user = models.User(
            username=request.json['username'],
            email=request.json['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return models.user_schema.dump(new_user)

    def delete(self):
        models.User.query.delete()
        db.session.commit()
        return '', 204

class UserResource(Resource):
    def get(self, user_id):
        user = models.User.query.get_or_404(user_id)
        return models.user_schema.dump(user)

    def patch(self, user_id):
        user = models.User.get_or_404(user_id)

        if 'username' in request.json:
            user.username = request.json['user']
        if 'email' in request.json:
            user.email = request.json['email']
        
        db.session.commit()
        return models.user_schema.dump(user)
    
    def delete(self, user_id):
        user = models.User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

@bp.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@bp.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404