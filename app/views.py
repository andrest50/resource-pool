import functools
from flask import Blueprint, render_template, jsonify, request, url_for
from app import models
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

@bp.route('/users', methods=['GET', 'POST'])
def users_data():
    users = models.User.query.all()
    if request.method == 'POST':
        users.append(request.users)
        return redirect(url_for('users_page'))
    print(users)
    return f'{users}'

@bp.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@bp.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404