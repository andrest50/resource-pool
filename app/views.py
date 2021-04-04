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
    resources = models.Resource.query.join(models.User, models.Resource.user_id==models.User.id)\
        .add_columns(models.Resource.url, 
                    models.Resource.category, 
                    models.Resource.resc_type, 
                    models.User.id, 
                    models.User.username, 
                    models.User.email)
    users = models.User.query.all()
    print(resources)
    for resource in resources:
        print(resource.url)
    return render_template('home.html', resources=resources, users=users)

@bp.route('/users_page')
def users_page():
    #models.test_db()
    users = models.User.query.all()
    print(users)
    for user in users:
        print(user.username)
        print(user.email)
    return render_template('users.html', users=users)

@bp.route('/layouts/header.html')
def header_component():
    page = request.args.get('active_page', None)
    print(page)
    return render_template('layouts/header.html', active_page=page)

@bp.route('/layouts/footer.html')
def footer_component():
    page = request.args.get('active_page', None)
    print(page)
    return render_template('layouts/footer.html', active_page=page)

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

class ResourceListResource(Resource):
    def get(self):
        resources = models.Resource.query.all()
        return models.resources_schema.dump(resources)

    def post(self):
        print(request.json)
        new_resource = models.Resource(
            url=request.json['url'],
            category=request.json['category'],
            resc_type=request.json['resc_type'],
            user_id=request.json['user_id']
        )
        print(new_resource)
        db.session.add(new_resource)
        db.session.commit()
        return models.resource_schema.dump(new_resource)

    def delete(self):
        models.Resource.query.delete()
        db.session.commit()
        return '', 204

@bp.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@bp.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404