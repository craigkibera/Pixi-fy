from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from extensions import db, bcrypt
from resources import HelloWorld
from authentication import SignUp, Login
from models import db, User, Post, Comment, Like, Follow, Profile

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
bcrypt.init_app(app)

migrate = Migrate(app, db)

# Initialize API
api = Api(app)

# Register your API resources
api.add_resource(HelloWorld, '/')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict_basic() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get_or_404(id)
        return jsonify(user.to_dict_basic()), 200
    except Exception as e:
        return jsonify({"error": "User not found"}), 404


@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    data = request.get_json()
    try:
        user = User.query.get_or_404(id)
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        db.session.commit()
        return jsonify(user.to_dict_basic()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": "User not found"}), 404


@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.all()
        return jsonify([post.to_dict() for post in posts]), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch posts"}), 500


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    try:
        new_post = Post(title=data['title'], body=data['body'], author_id=data['author_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    try:
        post = Post.query.get_or_404(id)
        return jsonify(post.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Post not found"}), 404


@app.route('/posts/<int:id>', methods=['PATCH'])
def update_post(id):
    data = request.get_json()
    try:
        post = Post.query.get_or_404(id)
        if 'title' in data:
            post.title = data['title']
        if 'body' in data:
            post.body = data['body']
        db.session.commit()
        return jsonify(post.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Post not found"}), 404


@app.route('/comments', methods=['GET'])
def get_comments():
    try:
        comments = Comment.query.all()
        return jsonify([comment.to_dict() for comment in comments]), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch comments"}), 500


@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    try:
        new_comment = Comment(body=data['body'], post_id=data['post_id'])
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    try:
        comment = Comment.query.get_or_404(id)
        return jsonify(comment.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Comment not found"}), 404


@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    try:
        comment = Comment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Comment not found"}), 404


@app.route('/profiles', methods=['GET'])
def get_profiles():
    try:
        profiles = Profile.query.all()
        return jsonify([profile.to_dict() for profile in profiles]), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch profiles"}), 500


@app.route('/profiles', methods=['POST'])
def create_profile():
    data = request.get_json()
    try:
        new_profile = Profile(location=data['location'], profile_image=data['profile_image'],
                              website=data['website'], bio=data['bio'], user_id=data['user_id'])
        db.session.add(new_profile)
        db.session.commit()
        return jsonify(new_profile.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/profiles/<int:id>', methods=['GET'])
def get_profile(id):
    try:
        profile = Profile.query.get_or_404(id)
        return jsonify(profile.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Profile not found"}), 404


@app.route('/profiles/<int:id>', methods=['PATCH'])
def update_profile(id):
    data = request.get_json()
    try:
        profile = Profile.query.get_or_404(id)
        if 'location' in data:
            profile.location = data['location']
        if 'bio' in data:
            profile.bio = data['bio']
        db.session.commit()
        return jsonify(profile.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/likes', methods=['POST'])
def like_post():
    data = request.get_json()
    try:
        new_like = Like(user_id=data['user_id'], post_id=data['post_id'])
        db.session.add(new_like)
        db.session.commit()
        return jsonify(new_like.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/likes/<int:id>', methods=['DELETE'])
def unlike_post(id):
    try:
        like = Like.query.get_or_404(id)
        db.session.delete(like)
        db.session.commit()
        return jsonify({"message": "Like removed"}), 200
    except Exception as e:
        return jsonify({"error": "Like not found"}), 404


@app.route('/follows', methods=['POST'])
def follow_user():
    data = request.get_json()
    try:
        new_follow = Follow(follower_id=data['follower_id'], followed_id=data['followed_id'])
        db.session.add(new_follow)
        db.session.commit()
        return jsonify(new_follow.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/follows/<int:id>', methods=['DELETE'])
def unfollow_user(id):
    try:
        follow = Follow.query.get_or_404(id)
        db.session.delete(follow)
        db.session.commit()
        return jsonify({"message": "Unfollowed user"}), 200
    except Exception as e:
        return jsonify({"error": "Follow not found"}), 404


@app.route('/follows', methods=['GET'])
def get_follows():
    try:
        follows = Follow.query.all()
        return jsonify([follow.to_dict() for follow in follows]), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch follows"}), 500


if __name__ == '__main__':
    app.run(debug=True)
