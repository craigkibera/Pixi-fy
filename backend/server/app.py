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

    title = data.get('title')
    body = data.get('body')
    author_id = data.get('author_id')
    image_url = data.get('image_url')  

    if not title or not body or not author_id:
        return jsonify({"error": "Title, body, and author_id are required."}), 400

    try:
        new_post = Post(
            title=title,
            body=body,
            author_id=author_id,
            image_url=image_url
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.to_dict()), 201

    except ValueError as ve:
        return jsonify({"validation_error": str(ve)}), 422
    except Exception as e:
        return jsonify({"error": "Failed to create post", "details": str(e)}), 500



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
        new_comment = Comment(
            body=data['body'],
            post_id=data['post_id'],
            user_id=data['user_id'],  # 👈 INCLUDE THIS
            parent_comment_id=data.get('parent_comment_id')  # optional
        )
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


@app.route('/profiles/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        # Look up a profile by the user_id field.
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile:
            return jsonify(profile.to_dict()), 200
        else:
            # Return an empty object if no profile exists for that user.
            return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500




@app.route('/profiles/<int:user_id>', methods=['PATCH'])
def update_profile(user_id):
    data = request.get_json()
    try:
        # Retrieve the profile by user_id
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({"error": "Profile not found"}), 404

        # Update fields if provided in data
        if 'location' in data:
            profile.location = data['location']
        if 'bio' in data:
            profile.bio = data['bio']
        if 'website' in data:
            profile.website = data['website']
        if 'profile_image' in data:
            profile.profile_image = data['profile_image']

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

@app.route('/likes', methods=['GET'])
def get_likes():
    try:
        likes = Like.query.all()
        return jsonify([like.to_dict() for like in likes]), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch likes"}), 500


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

    # Check required fields
    if not data.get('follower_id') or not data.get('followed_id'):
        return jsonify({"error": "follower_id and followed_id are required."}), 400

    # Prevent a user from following themselves
    if data['follower_id'] == data['followed_id']:
        return jsonify({"error": "User cannot follow themselves."}), 400

    try:
        # Check if follow relationship already exists
        existing_follow = Follow.query.filter_by(
            follower_id=data['follower_id'],
            followed_id=data['followed_id']
        ).first()
        if existing_follow:
            return jsonify({"error": "Already following this user."}), 400

        new_follow = Follow(
            follower_id=data['follower_id'],
            followed_id=data['followed_id']
        )
        db.session.add(new_follow)
        db.session.commit()
        return jsonify(new_follow.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/follows', methods=['GET'])
def get_follows():
    try:
        follower_id = request.args.get('follower_id', type=int)
        followed_id = request.args.get('followed_id', type=int)
        
        query = Follow.query
        if follower_id:
            query = query.filter_by(follower_id=follower_id)
        if followed_id:
            query = query.filter_by(followed_id=followed_id)
            
        follows = query.all()
        return jsonify([follow.to_dict() for follow in follows]), 200
    except Exception as e:
        return jsonify({"error": "Unable to fetch follows", "details": str(e)}), 500

@app.route('/follows/<int:follow_id>', methods=['DELETE'])
def delete_follow(follow_id):
    try:
        follow = Follow.query.get_or_404(follow_id)
        db.session.delete(follow)
        db.session.commit()
        return jsonify({"message": "Follow removed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
