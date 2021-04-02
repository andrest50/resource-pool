from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
from app import db, ma
import json

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

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

def test_db():
    #Base.metadata.create_all()
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    session.add(admin)
    session.add(guest)
    session.commit()

# Create tables.
#Base.metadata.create_all(bind=engine)