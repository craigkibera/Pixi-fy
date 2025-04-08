from flask import Flask, jsonify, request
from extensions import db
from models import User, Post, Like, Follow, Comment, Profile
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixify.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Initialize the database with the Flask app
db.init_app(app)

# Route to get all likes
@app.route('/likes', methods=['GET'])
def get_likes():
    likes = Like.query.all()
    return jsonify([like.to_dict() for like in likes])

# Route to get a specific like by its ID
@app.route('/like/<int:id>', methods=['GET'])
def get_like(id):
    like = Like.query.get(id)
    if like:
        return jsonify(like.to_dict())
    return jsonify({"message": "Like not found"}), 404

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict_basic() for user in users])

# Route to get a specific user by its ID
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict_basic())
    return jsonify({"message": "User not found"}), 404

# Route to create a new user (POST)
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict_basic()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Route to follow a user (POST)
@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    follower_id = data['follower_id']
    followed_id = data['followed_id']

    if follower_id == followed_id:
        return jsonify({"message": "User cannot follow themselves."}), 400

    existing_follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if existing_follow:
        return jsonify({"message": "You are already following this user."}), 400

    try:
        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.session.add(follow)
        db.session.commit()
        return jsonify(follow.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Route to get a specific post by its ID
@app.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    if post:
        return jsonify(post.to_dict())
    return jsonify({"message": "Post not found"}), 404

# Route to create a new post (POST)
@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    try:
        new_post = Post(
            title=data['title'],
            body=data['body'],
            author_id=data['author_id']
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Route to add a comment to a post (POST)
@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    try:
        new_comment = Comment(
            body=data['body'],
            post_id=data['post_id'],
            user_id=data['user_id'],
            parent_comment_id=data.get('parent_comment_id')
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Route to get a user's profile
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if profile:
        return jsonify(profile.to_dict())
    return jsonify({"message": "Profile not found"}), 404

# Route to update a user's profile (PUT)
@app.route('/profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    data = request.get_json()
    profile.location = data.get('location', profile.location)
    profile.profile_image = data.get('profile_image', profile.profile_image)
    profile.website = data.get('website', profile.website)
    profile.bio = data.get('bio', profile.bio)

    db.session.commit()
    return jsonify(profile.to_dict())

# Route to create a new like (POST)
@app.route('/like', methods=['POST'])
def create_like():
    data = request.get_json()
    try:
        new_like = Like(
            user_id=data['user_id'],
            post_id=data['post_id']
        )
        db.session.add(new_like)
        db.session.commit()
        return jsonify(new_like.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 400

# Home route to check if the app is working
@app.route('/')
def home():
    return "Pixi-Fy API is running."




if __name__ == '__main__':
    app.run(debug=True)
