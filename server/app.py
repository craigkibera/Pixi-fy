from flask import Flask
from flask_restful import Api
from resources import HelloWorld
from models import db
from flask_migrate import Migrate

app = Flask(__name__)
# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pixify.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize extension
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# Add the HelloWorld resource to the API
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
