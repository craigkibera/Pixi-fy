from extensions import db, bcrypt  # Import db and bcrypt from extensions.py
from sqlalchemy_serializer import SerializerMixin





class User(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128), nullable=False)  
    first_name = db.Column(db.String(100), nullable=True)  
    last_name = db.Column(db.String(100), nullable=True)  
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())  
    
    #Serialization rules.



    #Attribute Validations.


    
    def __repr__(self):
        return f'<User {self.username}>'


    #working on password.
    def set_password(self, password):
        # Hash the password using bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return bcrypt.check_password_hash(self.password_hash, password)

if __name__ == '__main__':
    app.run(debug=True)



