from flask_restful import Resource
from flask import request ,make_response, jsonify
from models import User  # Import your models if you're interacting with a database

# This is a simple resource that returns a "Hello, World!" message.
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World GROUP 10!'}

#sign up resource
class Sign_up(Resource):
    def post(self):
        #recieve our data.
        data = request.get_json()
        
        user


