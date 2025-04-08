from flask import Flask, request, jsonify
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

# USERS
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@app.route('/users/<int:user_id>/follow/<int:followed_id>', methods=['POST'])
def follow_user(user_id, followed_id):
    user = User.query.get_or_404(user_id)
    followed = User.query.get_or_404(followed_id)

    if Follow.query.filter_by(follower_id=user.id, followed_id=followed.id).first():
        return jsonify({'message': 'Already following'}), 400

    follow = Follow(follower_id=user.id, followed_id=followed.id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': f'{user.username} now follows {followed.username}'}), 200

@app.route('/users/<int:user_id>/unfollow/<int:followed_id>', methods=['DELETE'])
def unfollow_user(user_id, followed_id):
    follow = Follow.query.filter_by(follower_id=user_id, followed_id=followed_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'message': 'Unfollowed successfully'}), 200
    return jsonify({'message': 'Not following'}), 404

@app.route('/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    followers = Follow.query.filter_by(followed_id=user_id).all()
    return jsonify([User.query.get(f.follower_id).to_dict() for f in followers]), 200

@app.route('/users/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    following = Follow.query.filter_by(follower_id=user_id).all()
    return jsonify([User.query.get(f.followed_id).to_dict() for f in following]), 200

# POSTS
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(
        content=data['content'],
        media_url=data.get('media_url'),
        user_id=data['user_id']
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    post.content = data.get('content', post.content)
    post.media_url = data.get('media_url', post.media_url)
    db.session.commit()
    return jsonify(post.to_dict()), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'}), 200

@app.route('/users/<int:user_id>/feed', methods=['GET'])
def user_feed(user_id):
    following = Follow.query.filter_by(follower_id=user_id).all()
    followed_ids = [f.followed_id for f in following] + [user_id]
    posts = Post.query.filter(Post.user_id.in_(followed_ids)).order_by(Post.timestamp.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

# COMMENTS
@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    comment = Comment(
        content=data['content'],
        user_id=data['user_id'],
        post_id=data['post_id']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify([comment.to_dict() for comment in post.comments]), 200

# LIKES
@app.route('/likes', methods=['POST'])
def create_like():
    data = request.get_json()
    like = Like(
        reaction_type=data.get('reaction_type', 'like'),
        user_id=data['user_id'],
        post_id=data['post_id']
    )
    db.session.add(like)
    db.session.commit()
    return jsonify(like.to_dict()), 201

@app.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify([like.to_dict() for like in post.likes]), 200

# MAIN
if __name__ == '__main__':
    app.run(debug=True)

