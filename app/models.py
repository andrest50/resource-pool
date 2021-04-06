from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from marshmallow import Schema, fields
from app.database import Base
from app import db, ma
import json

class Resource(db.Model):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    url = Column(String(80), unique=False, nullable=False)
    category = Column(String(80), nullable=False)
    resc_type = Column(String(80), nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        resource_dict = {
            'id': self.id,
            'url': self.url,
            'category': self.category,
            'resc_type': self.resc_type,
            'user_id': self.user_id
        }
        return json.dumps(resource_dict)

class ResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'url', 'category', 'resc_type', 'user_id')
        model = Resource
        include_fk = True
        sqla_session = db.session

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    resources = db.relationship('Resource', backref='user')

    def __repr__(self):
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        return json.dumps(user_dict)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ('id', 'username', 'email')
        model = User
        sqla_session = db.session

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    #resources = ma.auto_field()
    resources = ma.Nested(ResourceSchema, many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def test_db():
    #Base.metadata.create_all()
    admin = User(username='admin', email='admin@example.com', password="testing")
    guest = User(username='guest', email='guest@example.com', password="testing2")
    session.add(admin)
    session.add(guest)
    session.commit()

# Create tables.
#Base.metadata.create_all(bind=engine)