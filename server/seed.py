from app import db, app, bcrypt  # Import app and bcrypt from app.py
from models import User  # Import User from models.py
from sqlalchemy.sql import func  # Import func for database functions

with app.app_context():
    # Delete all existing users before seeding new data
    db.session.query(User).delete()  # This deletes all records in the User table
    db.session.commit()  # Commit the deletion to the database
    print('All existing users have been deleted.')

    # Create 10 users with hashed passwords
    user1 = User(
        username='john_doe',
        email='john@example.com',
        password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
        first_name='John',
        last_name='Doe',
        date_created=func.now()
    )
    user2 = User(
        username='jane_doe',
        email='jane@example.com',
        password_hash=bcrypt.generate_password_hash('securepassword').decode('utf-8'),
        first_name='Jane',
        last_name='Doe',
        date_created=func.now()
    )
    user3 = User(
        username='alice_smith',
        email='alice@example.com',
        password_hash=bcrypt.generate_password_hash('alicepassword').decode('utf-8'),
        first_name='Alice',
        last_name='Smith',
        date_created=func.now()
    )
    user4 = User(
        username='bob_jones',
        email='bob@example.com',
        password_hash=bcrypt.generate_password_hash('bobpassword').decode('utf-8'),
        first_name='Bob',
        last_name='Jones',
        date_created=func.now()
    )
    user5 = User(
        username='carol_white',
        email='carol@example.com',
        password_hash=bcrypt.generate_password_hash('carolpassword').decode('utf-8'),
        first_name='Carol',
        last_name='White',
        date_created=func.now()
    )
    user6 = User(
        username='dan_black',
        email='dan@example.com',
        password_hash=bcrypt.generate_password_hash('danpassword').decode('utf-8'),
        first_name='Dan',
        last_name='Black',
        date_created=func.now()
    )
    user7 = User(
        username='eva_martin',
        email='eva@example.com',
        password_hash=bcrypt.generate_password_hash('evapassword').decode('utf-8'),
        first_name='Eva',
        last_name='Martin',
        date_created=func.now()
    )
    user8 = User(
        username='fred_brown',
        email='fred@example.com',
        password_hash=bcrypt.generate_password_hash('fredpassword').decode('utf-8'),
        first_name='Fred',
        last_name='Brown',
        date_created=func.now()
    )
    user9 = User(
        username='grace_davis',
        email='grace@example.com',
        password_hash=bcrypt.generate_password_hash('gracepassword').decode('utf-8'),
        first_name='Grace',
        last_name='Davis',
        date_created=func.now()
    )
    user10 = User(
        username='henry_garcia',
        email='henry@example.com',
        password_hash=bcrypt.generate_password_hash('henrypassword').decode('utf-8'),
        first_name='Henry',
        last_name='Garcia',
        date_created=func.now()
    )

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)
    db.session.add(user9)
    db.session.add(user10)
    
    # Commit the session to save the users to the database
    db.session.commit()
    print('Database seeded with users successfully.')
