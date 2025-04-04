from flask_restful import Resource
from flask import request  # If you need to handle request data (e.g., POST requests)
from models import User  # Import your models if you're interacting with a database

# This is a simple resource that returns a "Hello, World!" message.
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World GROUP 10!'}
