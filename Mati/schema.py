from Mati import db, app, route, marshmallow
from Mati.model import (User,
                        Post,
                        PostLike,
                        followers)
import os


class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 
                  'username', 
                  'email')


class PostSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 
                  'imagePath', 
                  'body',
                  'timestamp',
                  'author_id')