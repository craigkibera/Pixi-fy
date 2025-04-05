from app import app, db
from models import User

# Ensure you're running inside the app context
with app.app_context():
    
    db.drop_all()
    db.create_all()

    # Create sample users
    user1 = User(
        name="Engineer Collins",
        email="collins@example.com",
        password_hash="hashedpassword123"  # Use a proper hashing method in real apps
    )

    user2 = User(
        name="Lesile",
        email="lesile@example.com",
        password_hash="anotherhashedpassword456"
    )

    # Add to session and commit
    db.session.add_all([user1, user2])
    db.session.commit()

    print("Database seeded successfully!")
