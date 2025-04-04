from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin



# Initialize SQLAlchemy
db = SQLAlchemy()

# Example Defining the User model

# class User(db.Model, SerializerMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)  
#     password-hash = db.Column(db.String(128), nullable=False)