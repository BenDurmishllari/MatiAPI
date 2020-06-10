from Mati import db, app, route, login_manager
from datetime import datetime
from flask_login import UserMixin

followers = db.Table(
                      
                    'followers',
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

likes = db.Table(
                      
                'likes',
                db.Column('account_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
                                secondary = followers,
                                primaryJoin = (followers.c.follower_id == id),
                                secondaryJoin = (followers.c.followed_id == id),
                                backref = db.backref('followers', lazy = 'dynamic'),
                                lazy = 'dynamic')