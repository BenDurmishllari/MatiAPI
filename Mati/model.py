from Mati import db, app, route, login_manager
from datetime import datetime
from flask_login import UserMixin


''' Load the user id and store it in the session '''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Holds user's id for the follower and followed cases
followers = db.Table(
                      
                    'followers',
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin):

    ''' 
        User class, it used for creating User object also,
        its inherit from UserMixin as well in order to use the default methods that Flask login require 
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Provide relationship between users, 
    # it links User instances to other User instances
    followed = db.relationship('User',
                                secondary = followers,
                                primaryjoin = (followers.c.follower_id == id),
                                secondaryjoin = (followers.c.followed_id == id),
                                backref = db.backref('followers', lazy = 'dynamic'),
                                lazy = 'dynamic')

    # Relationship with PostLike 
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id=self.id,post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}','{self.password}'')"

class Post(db.Model):
    
    ''' Post class, it used for creating Post object '''

    id = db.Column(db.Integer, primary_key=True)
    imagePath = db.Column(db.Text, nullable = False)
    body = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    # Relationship with the user that create the post
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.id}','{self.imagePath}', '{self.body}','{self.timestamp},'{self.author_id}'')"

class PostLike(db.Model):

    ''' PostLike class, it holds user.id and post.id for post like cases '''
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"PostLike('{self.user_id}','{self.post_id}'')"


