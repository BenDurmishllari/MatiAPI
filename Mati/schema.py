from Mati import (db, 
                  app, 
                  route, 
                  marshmallow)
from Mati.model import (User,
                        Post)
                       
import os

''' Using Marshmallow for object serialization/deserialization '''

class UserSchema(marshmallow.Schema):
    class Meta:
        ''' User uoutput format '''
        fields = ('id', 
                  'username', 
                  'email')


class PostSchema(marshmallow.Schema):
    class Meta:
        ''' Post output format '''
        fields = ('id', 
                  'imagePath', 
                  'body',
                  'timestamp',
                  'author_id')