import functools
from flask import Blueprint, render_template, jsonify, request
from app import models
import json

bp = Blueprint('files', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/home')
def home_page():
    #models.test_db()
    return render_template('home.html')

@bp.route('/users')
def users_page():
    #models.test_db()
    users = models.User.query.all()
    print(users)
    for user in users:
        print(user.username)
        print(user.email)
    return render_template('users.html', users=users)

@bp.route('/users_data', methods=['GET'])
def get_users_data():
    users = models.User.query.all()
    print("here")
    print(users)
    return json.dumps(users[0])

@bp.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@bp.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404