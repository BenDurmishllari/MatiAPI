from Mati import (app, 
                  db, 
                  bcrypt, 
                  marshmallow, 
                  UPLOAD_FOLDER,
                  ALLOWED_EXTENSIONS)
from Mati.model import (User,
                        Post,
                        PostLike,
                        followers)
from Mati.schema import (UserSchema, 
                        PostSchema)
from Mati.validator import (EmailValidator,
                            UniqueUsername)
from flask import (request, 
                   abort,
                   session, 
                   jsonify,
                   json)
from flask_login import (login_user, 
                         logout_user, 
                         login_required, 
                         current_user)
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os


emailValidator = EmailValidator()
uniqueUsername = UniqueUsername()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['POST'])
def login():
    
    '''Login route,  it is used to login the user, and to check if user is already authenticated'''

    if current_user.is_authenticated:
        return jsonify({'message': 'You\'re already login'})
    
    else:
        if request.method == 'POST':
            email = request.json['email']
            password = request.json['password']
            user = User.query.filter_by(email = email).first()
            
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return user_schema.jsonify(current_user)
            else:
                return jsonify({'message': 'Wrong credentials!'})


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'You have logout'})

@app.route('/register', methods=['POST'])
def register():

    '''Register route, it creates users accounts'''

    if request.method == 'POST':

        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        checkEmail = emailValidator.checkEmail(email)
        checkUserName = uniqueUsername.checkUsername(username)

        if checkEmail == "Email is valid!" and checkUserName == "Username don't exist":

            hased_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(username=username,
                            email = email,
                            password = hased_password)
            
            db.session.add(new_user)
            db.session.commit()

            return user_schema.jsonify(new_user)
        else:
            if checkEmail == "Email is not valid":
                return jsonify({'message': 'Please add a valid email'})
            if checkUserName == "Username exist":
                return jsonify({'message': 'Username exist, please use another username'})


def allowed_file(filename):

    ''' Check if the file extenxion is valid '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/newPost', methods=['POST'])
@login_required
def new_post():

    ''' New post route, it is used to create users posts '''

    if request.method == 'POST':
        
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'message': 'No selected file'})
        
        body = request.form['body']

        if len(body) > 100:
            return jsonify({'message': 'Image caption, must be approximately 100 characters'})
        else:
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                imagePath = '/static/uploadImages/' + str(filename)

                new_post = Post(imagePath = imagePath,
                                body = body,
                                author=current_user)
                
                db.session.add(new_post)
                db.session.commit()

                return post_schema.jsonify(new_post)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):

    ''' Follow route, it is used for following users '''

    if request.method == 'POST':

        user = User.query.filter_by(username=username).first()

        if user is None:
            return jsonify({'message': 'User' + ' ' + username + ' ' + 'not found!'})
        if current_user.is_following(user) == True:
            return jsonify({'message': 'You already follow' + ' ' + username})
        else:
            follow = current_user.follow(user)
            if current_user == user:
                return jsonify({'message': 'You can\'t follow yourself'})
            else:
                db.session.add(follow)
                db.session.commit()
                return jsonify({'message': 'You are now following' + ' ' + username})
    


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):

    ''' Unfollow route, it is used for unfollowing users '''
    
    if request.method == 'POST':

        user = User.query.filter_by(username=username).first()

        if user is None:
            return jsonify({'message': 'User' + ' ' + username + ' ' + 'not found!'})
        if current_user.is_following(user) == False:
            return jsonify({'message': 'You never followed' + ' ' + username})
        else:
            unfollow = current_user.unfollow(user)
            db.session.add(unfollow)
            db.session.commit()
            return jsonify({'message': 'You have stopped following' + ' ' + username})


@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_action(post_id):

    ''' Like route, it is used to like a post '''
    
    if request.method == 'POST':

        post = Post.query.filter_by(id=post_id).first()

        if post is None:
            return jsonify({'message': 'Post not found!'})
        if current_user.has_liked_post(post) == True:
            return jsonify({'message': 'You already liked this post'})
        else:
            current_user.like_post(post)
            db.session.commit()
            return jsonify({'message': 'You like the post'})


@app.route('/unlike/<int:post_id>', methods=['POST'])
@login_required
def unlike_action(post_id):

    ''' Like route, it is used to unlike a post '''

    if request.method == 'POST':

        post = Post.query.filter_by(id=post_id).first()

        if post is None:
            return jsonify({'message': 'Post not found!'})
        if current_user.has_liked_post(post) == False:
            return jsonify({'message': 'You never liked this post'})
        else:
            current_user.unlike_post(post)
            db.session.commit()
            return jsonify({'message': 'You unlike the post'})


@app.route('/followedUsersPosts', methods=['GET'])
@login_required
def followed_users_posts():

    ''' 
        Followed users posts route, 
        it returns the list of images for the current user (most recent first, limited to users following) 
    '''

    if request.method == 'GET':
        try:
            followedPosts = Post.query.join(followers, 
                                            followers.c.followed_id == Post.author_id) \
                                            .filter(followers.c.follower_id == current_user.id) \
                                            .order_by(Post.timestamp.desc()).all()
            if not followedPosts:
                return jsonify({'message': 'Your followed users don\'t have any post yet'})
            else:
                responseData = []

                for followedPost in followedPosts:

                    followedPostData = {}
                    followedPostData['id'] = followedPost.id
                    followedPostData['image'] = followedPost.imagePath
                    followedPostData['body'] = followedPost.body
                    followedPostData['timestamp'] = followedPost.timestamp
                    followedPostData['author'] = followedPost.author.username
                    responseData.append(followedPostData)
                    
                return jsonify({'List of images for the current user (most recent first, limited to users following)': responseData})
        except:
            return jsonify({'message': 'Something went wrong, please try again!'})

@app.route('/posts', methods=['GET'])
@login_required
def get_all_posts():

    ''' Get all posts route, it returns the list of all posts (ordered by likes) '''

    if request.method == 'GET':

        posts = db.session.query(Post).outerjoin(PostLike).group_by(Post.id) \
                                                          .order_by(func.count().desc()).all()
        if not posts:
            return jsonify({'message': 'No posts yet'})
        else:
            responseData = []

            for post in posts:

                postData = {}
                postData['id'] = str(post.id)
                postData['body'] = post.body
                postData['imagePath'] = post.imagePath
                postData['timestamp'] = post.timestamp
                postData['author'] = post.author.username
                postData['likes'] = str(post.likes.count())
                responseData.append(postData)
            
            return jsonify({'List of all posts (ordered by likes)': responseData})



@app.route('/users', methods=['GET'])
@login_required
def get_all_users():

    ''' 
        Get all users route, 
        it returns the list of all users (including information on the number of following and followers). 
    '''
    
    if request.method == 'GET':

        users = User.query.all()

        if not users:
            return jsonify({'message': 'No recorded users yet'})
        else:
            responseData = []

            for user in users:

                userData = {}
                userData['id'] = user.id
                userData['username'] = user.username
                userData['email'] = user.email
                userData['posts'] = str(user.posts.count())
                userData['following'] = str(user.followed.count()) 
                userData['followers'] = str(user.followers.count())
                responseData.append(userData)
            
            return jsonify({'List of all users (including information on the number of following and followers)': responseData})
