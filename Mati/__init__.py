from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Init app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mati.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init Bcrypt
bcrypt = Bcrypt(app)

# Init Marshmallow
marshmallow = Marshmallow(app)

# Configs for upload folder
UPLOAD_FOLDER = './Mati/static/uploadImages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CORS(app)


# Init LoginManager
login_manager = LoginManager(app)



from Mati import route
from Mati.model import User, Post, PostLike, followers
from Mati.schema import UserSchema
