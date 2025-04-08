from flask import request
from flask_restful import Resource
from extensions import bcrypt
from models import db, User


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username and password are required"}, 400
        
        if not email or not first_name or not last_name:
            return {"message": "Email, first name, and last name are required"}, 400
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "Email already exists"}, 409
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, first_name=first_name, last_name=last_name, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User created successfully"}, 201
        

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"message": "Email and password are required"}, 400
        
        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return {"message": "Invalid credentials"}, 401
        
        return {"message": "Login successful"}, 200

    def get(self):
        return {"connected": "on"}





