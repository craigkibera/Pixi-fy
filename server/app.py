from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from extensions import db, bcrypt  # Import from extensions.py
from resources import HelloWorld  # Import your resources (e.g., HelloWorld)
from authentication import SignUp, Login

# Create your app instance
app = Flask(__name__)

# Configure the app (for example, database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the extensions
db.init_app(app)
bcrypt.init_app(app)

# Set up migration
migrate = Migrate(app, db)

# Initialize API
api = Api(app)

# Register your API resources
api.add_resource(HelloWorld, '/')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')


if __name__ == '__main__':
    app.run(debug=True)

# Optionally, add more routes or resources here
