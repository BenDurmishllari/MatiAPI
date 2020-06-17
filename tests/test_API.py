import os
import requests
import sys
import unittest
print(sys.path)
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from Mati import app, db
from flask_sqlalchemy import SQLAlchemy
from Mati.model import User, Post, PostLike, followers

url = 'http://localhost:5000'

class TestStringMethods(unittest.TestCase):

    ''' Test Class, used for testing different cases based on the API '''

    # db 
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI']

    # Ensure that add a new user works correctly
    def test_AddUser(self):

        response = requests.post(url = url + '/register', json={ "username": "unittest1",
                                                      "email": "unittest1@gmail.com", 
                                                      "password": "unittest1"})
        user = User.query.filter_by(username = 'unittest1').first()
        self.assertIsNot(user, None)
    
    # Ensure that returns the correct user data
    def test_LoingUser(self):

        hardcodeUserData = {"email": "unittest1@gmail.com", 
                            "id": 8, 
                            "username": "unittest1"}
        response = requests.post(url=url+'/login', json={ "email": "unittest1@gmail.com",
                                                          "password": "unittest1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), hardcodeUserData)

    # Test if follow and unfollow works correctly, and based on the targeted users
    def test_FollowUnfollow(self):

        user_1 = User.query.filter_by(username='unittest1').first()
        user_2 = User.query.filter_by(username='mariza').first()

        self.assertIsNone(user_1.unfollow(user_2))
        follow_1 = user_1.follow(user_2)
        db.session.add(follow_1)
        db.session.commit()
        self.assertIsNone(user_1.follow(user_2)) 
        self.assertTrue(user_1.is_following(user_2))
        self.assertTrue(user_1.followed.count()==1)
        self.assertTrue(user_2.followers.count()==1)
        unfollow_1 = user_1.unfollow(user_2)
        self.assertTrue(unfollow_1)
        db.session.add(unfollow_1)
        db.session.commit()
        self.assertIsNotNone(user_1.is_following(user_2))
        self.assertTrue(user_1.followed.count() == 0)
        self.assertTrue(user_2.followers.count() == 0)
         


if __name__ == '__main__':
    unittest.main()

