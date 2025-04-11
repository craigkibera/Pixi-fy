# Pixi-fy
Pixi-fy is a social media platform designed to connect users through posts, comments, likes, and follows. It includes features for user authentication, profile management, and content sharing.

## Features

### User Authentication
- **Sign Up**: Users can create an account by providing a username, email, first name, last name, and password.
- **Login**: Users can log in using their email and password. Passwords are securely hashed using bcrypt.

### User Profiles
- Each user has a profile with the following attributes:
    - Location
    - Profile image
    - Website
    - Bio
- Profiles are linked to users and can be updated or deleted.

### Posts
- Users can create posts with a title, body, and optional image.
- Posts are associated with their authors and include timestamps for creation and updates.

### Comments
- Users can comment on posts.
- Comments support nested replies, allowing users to engage in threaded discussions.

### Likes
- Users can like posts, with each like being unique to a user-post combination.

### Follows
- Users can follow other users.
- A user cannot follow themselves, and duplicate follows are prevented.

## Database Models
The application uses SQLAlchemy for database management. Key models include:
- **User**: Represents users with attributes like username, email, and password hash.
- **Profile**: Stores additional user information such as location and bio.
- **Post**: Represents user-generated content.
- **Comment**: Allows users to comment on posts and reply to other comments.
- **Like**: Tracks likes on posts.
- **Follow**: Tracks relationships between followers and followed users.

## API Endpoints
The application provides RESTful API endpoints for:
- User sign-up and login.
- CRUD operations for posts, comments, and profiles.
- Managing likes and follows.

## Setup Instructions
1. Clone the repository:
     ```bash
     git clone https://github.com/your-username/Pixi-fy.git
     cd Pixi-fy/server
     ```
2. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
3. Set up the database:
     ```bash
     flask db upgrade
     ```
4. Seed the database:
     ```bash
     python seed.py
     ```
5. Run the server:
     ```bash
     flask run
     ```

## Technologies Used
- **Backend**: Flask, Flask-RESTful
- **Database**: SQLAlchemy
- **Authentication**: bcrypt
- **Serialization**: sqlalchemy-serializer

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.