from extensions import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates



class Follow(db.Model, SerializerMixin):

    __tablename__="follows"

    __table_args__ = (
        db.UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),
    )

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    followed_user = db.relationship("User", foreign_keys=[followed_id], back_populates="followers")
    follower_user = db.relationship("User", foreign_keys=[follower_id], back_populates="following")

    def __repr__(self):
        return f"<Follow follower_id={self.follower_id}, followed_id={self.followed_id}, created_at={self.created_at}>"

    @validates('follower_id')
    def validate_follow(self, key, follower_id):
        if follower_id == self.followed_id:
            raise ValueError("User cannot follow themselves.")
        return follower_id


    def to_dict(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "created_at": self.created_at
        }


class User(db.Model,SerializerMixin):

    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128), nullable=False)  
    first_name = db.Column(db.String(100), nullable=True)  
    last_name = db.Column(db.String(100), nullable=True)  
    date_created = db.Column(db.DateTime, default=db.func.now())
    posts = db.relationship("Post", back_populates="author", cascade='all, delete-orphan')

    comments = db.relationship('Comment', back_populates='user', lazy=True) #added these line
    followers = db.relationship("Follow", foreign_keys=[Follow.followed_id], back_populates="followed_user")
    following = db.relationship("Follow", foreign_keys=[Follow.follower_id], back_populates="follower_user")

    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade='all, delete-orphan')
    likes = db.relationship("Like", back_populates="user", cascade='all, delete-orphan')
    #comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    serialize_rules = ("-password_hash", "-posts.author", "-profile.user")
    def __repr__(self):
        return f"<user {self.username}, {self.email}, {self.password_hash}, {self.first_name}, {self.last_name}, {self.date_created}>"
    
    def to_dict_basic(self):
        return{
            "id":self.id,
            "username":self.username,
            "email":self.email,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "date_created":self.date_created
        }
    
    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("username cannot be empty.")
        if len(username) < 3:
            raise ValueError("username must be 3 characters long.")
        return username

    @validates ("email")
    def validate_email(self, key, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        return email
        
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    


 
class Post(db.Model, SerializerMixin):
    __tablename__="posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
   # author_id = db.Column(db.Integer, db.ForeignKey('users.id'),back_populates="posts", nullable=False)
    comments = db.relationship("Comment", back_populates="post", cascade='all, delete-orphan' )
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship("User", back_populates="posts")
    likes = db.relationship("Like", back_populates="post", cascade='all, delete-orphan')
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    #comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    def __repr__(self):
        return f'<post {self.title}, {self.body}, {self.created_at}, {self.updated_at}, {self.author_id}>'

    def to_dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "body":self.body,
            "created_at":self.created_at,
            "updated_at":self.updated_at,
            "author_id":self.author_id
        }
    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("title cannot be empty.")
        if len(title) < 5:
                raise ValueError("title must be atleast 5 characters")
        return title
    
    @validates("body")
    def validate_body(self, key, body):
        if not body:
            raise ValueError("Body cannot be empty")
        if len(body) < 4:
            raise ValueError("The body must have atleast 4 characters long.")
        return body


class Comment(db.Model, SerializerMixin):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    replies= db.relationship("Comment", back_populates="parent_comment", cascade='all, delete-orphan')
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    parent_comment = db.relationship("Comment", remote_side=[id], back_populates="replies")
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    post = db.relationship("Post", back_populates="comments")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)# i added these line
    user = db.relationship("User", back_populates="comments")  #added these line
   
    def __repr__(self):
        return f"<comments {self.id}, {self.body}, {self.created_at}>"

    def to_dict(self):
        return{
        "id":self.id,
        "body":self.body,
        "created_at":self.created_at,
        "post_id": self.post_id,
        "user_id": self.user_id,
        "parent_comment":self.parent_comment,
        "replies": [reply.to_dict() for reply in self.replies]
    }

    @validates("body")
    def validate_body(self, key, body):
        if not body:
            raise ValueError("Body cannot be empty")
        if len(body) < 4:
            raise ValueError("The body must have atleast 4 characters long.")
        return body


class Profile(db.Model, SerializerMixin):
    __tablename__="profiles"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    bio =  db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),unique=True, nullable=False)
    user = db.relationship("User", back_populates="profile", uselist=False)

    @validates("location")
    def validate_location(self, key, location):
        if not location:
            raise ValueError("location cannot be empty")
        if len(location) < 4:
            raise ValueError("location must be atleast 4 characters long.")
        return location
    
    @validates("bio")
    def validate_bio(self, key, bio):
        if not bio:
            raise ValueError("bio cannot be empty.")
        if len(bio) < 30:
            raise ValueError("bio must be atleast 30 characters long.")
        return bio
    
    def __repr__(self):
        return f"<userprofile {self.id}, {self.location}, {self.profile_image}, {self.website}, {self.bio}>"
    
    def to_dict(self):
        return{
            "id":self.id,
            "location":self.location,
            "profile_image":self.profile_image,
            "website":self.website,
            "bio":self.bio,
            "user_id":self.user_id
        }

class Like(db.Model, SerializerMixin):
    __tablename__="likes"

    __table_args__ = (
    db.UniqueConstraint('user_id', 'post_id', name='_user_post_like_uc'),
)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
   # user = db.relationship("User", back_populates="likes", cascade='all, delete-orphan')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship("User", back_populates="likes")
    post = db.relationship("Post", back_populates="likes")

    def __repr__(self):
        return f"<like {self.id}, {self.created_at}>"
    
    def to_dict(self):
        return{
            "id":self.id,
            "created_at":self.created_at,
            "user_id":self.user_id,
            "post_id":self.post_id
        }
