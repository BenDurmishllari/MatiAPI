from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mati.db'

# database instantiation
db = SQLAlchemy(app)

# login manager instantiation
login_manager = LoginManager(app)
login_manager.login_view = 'login'

login_manager.login_message_category = 'info'


from Mati import route
from Mati.model import User, Post, PostLike, followers