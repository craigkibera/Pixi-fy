from app import app
from extensions import db
from models import User, Post, Comment, Profile, Follow, Like

def seed_database():
    with app.app_context():
        print("Deleting all records...")
        # Clear all tables in reverse order of dependency
        Like.query.delete()
        Comment.query.delete()
        Post.query.delete()
        Follow.query.delete()
        Profile.query.delete()
        User.query.delete()

        print("Creating users...")
        # Create users
        users = [
            User(
                username="irarubrian",
                email="brian.o.iraru@gmail.com",
                first_name="iraru",
                last_name="brian"
            ),
            User(
                username="irarubrian2",
                email="iraru.brian@gmail.com",
                first_name="brian",
                last_name="iraru"
            ),
            User(
                username="brivianbella",
                email="brivian.o@gmail.com",
                first_name="brivian",
                last_name="bella"
            )
        ]

        # Set passwords
        for user in users:
            user.set_password("password4040")

        db.session.add_all(users)
        db.session.commit()

        print("Creating profiles...")
        # Create profiles
        profiles = [
            Profile(
                location="New York",
                profile_image="https://plus.unsplash.com/premium_photo-1689568126014-06fea9d5d341?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                website="https://verpex.com/blog/marketing-tips/10-most-popular-types-of-websites",
                bio="Software engineer passionate about web development and open source.",
                user_id=users[0].id
            ),
            Profile(
                location="San Francisco",
                profile_image="https://plus.unsplash.com/premium_photo-1689568126014-06fea9d5d341?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                website="https://verpex.com/blog/marketing-tips/10-most-popular-types-of-websites",
                bio="Digital marketer with 5 years of experience in tech companies.",
                user_id=users[1].id
            ),
            Profile(
                location="Chicago",
                profile_image="https://plus.unsplash.com/premium_photo-1689568126014-06fea9d5d341?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                website="https://verpex.com/blog/marketing-tips/10-most-popular-types-of-websites",
                bio="Graphic designer and illustrator creating beautiful visuals.",
                user_id=users[2].id
            )
        ]
        db.session.add_all(profiles)
        db.session.commit()

        print("Creating posts...")
        # Create posts
        posts = [
            Post(
                title="My First Blog Post",
                body="This is the content of my first blog post. I'm excited to start blogging!",
                author_id=users[0].id
            ),
            Post(
                title="Web Development Tips",
                body="Here are some tips I've learned after 5 years of web development experience.",
                author_id=users[1].id
            ),
            Post(
                title="Design Principles",
                body="Key design principles every developer should know to create better UIs.",
                author_id=users[2].id
            )
        ]
        db.session.add_all(posts)
        db.session.commit()

        print("Creating comments...")
        # Create comments
        comments = [
            Comment(
                body="Great first post! Looking forward to more content.",
                post_id=posts[0].id,
                user_id=users[1].id
            ),
            Comment(
                body="Thanks for sharing these valuable tips!",
                post_id=posts[1].id,
                user_id=users[2].id
            ),
            Comment(
                body="I especially agree with point #3 about color theory.",
                post_id=posts[2].id,
                user_id=users[0].id
            )
        ]
        db.session.add_all(comments)
        db.session.commit()

        print("Creating follows...")
        # Create follows
        follows = [
            Follow(follower_id=users[0].id, followed_id=users[1].id),
            Follow(follower_id=users[1].id, followed_id=users[2].id),
            Follow(follower_id=users[2].id, followed_id=users[0].id)
        ]
        db.session.add_all(follows)
        db.session.commit()

        print("Creating likes...")
        # Create likes
        likes = [
            Like(user_id=users[0].id, post_id=posts[1].id),
            Like(user_id=users[1].id, post_id=posts[2].id),
            Like(user_id=users[2].id, post_id=posts[0].id)
        ]
        db.session.add_all(likes)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()