from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
import json

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        #return f'<User {self.username}>'
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        return json.dumps(user_dict)

def test_db():
    Base.metadata.create_all()
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    session.add(admin)
    session.add(guest)
    session.commit()

# Create tables.
#Base.metadata.create_all(bind=engine)