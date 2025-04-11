from flask import request
from flask_restful import Resource
from extensions import bcrypt
from models import db, User


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username   = data.get('username')
        email      = data.get('email')
        first_name = data.get('first_name')
        last_name  = data.get('last_name')
        password   = data.get('password')

        # required‐field checks
        if not username or not password:
            return {"message": "Username and password are required"}, 400

        if not email or not first_name or not last_name:
            return {"message": "Email, first name, and last name are required"}, 400

        # ensure unique email
        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 409

        # create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # return id + safe user fields
        return {
            "message": "User created successfully",
            "user": {
                "id":         new_user.id,
                "username":   new_user.username,
                "email":      new_user.email,
                "first_name": new_user.first_name,
                "last_name":  new_user.last_name
            }
        }, 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        email    = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return {"message": "Invalid credentials"}, 401

        # at this point you might also issue a JWT or session token
        return {
            "message": "Login successful",
            "user": {
                "id":         user.id,
                "username":   user.username,
                "email":      user.email,
                "first_name": user.first_name,
                "last_name":  user.last_name
            }
        }, 200