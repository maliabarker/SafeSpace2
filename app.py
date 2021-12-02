from flask import Flask, render_template, request, session, redirect, url_for
from flask.helpers import url_for
from flask_pymongo import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt

CONNECTION_STRING = 'mongodb+srv://maliabarker:tpofbawf@safespace.8qywl.mongodb.net/safespace?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_default_database()
users = db.users
posts = db.posts

app = Flask(__name__)
app.secret_key = '9a5c0aaf287745d3b21371fb097bb5a22e6da0e9c8fb3bc39e34474f2f400f57'

@app.route('/')
def index():
    """Return Landing Page"""
    session['email']=None
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    post = posts.find()
    if request.method=='POST':
        form_name = request.form['form-name']
        if form_name == 'form1':
            email = request.form.get('email')
            email_found = users.find_one({'email': email})

            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            if email_found:
                message = 'There is already an account with this email'
                return render_template('index.html', message=message)
            elif password1 != password2:
                message = 'Passwords do not match, please re-enter passwords'
                return render_template('index.html', message=message)
            else:
                avatar = request.form['options']
                hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
                user = {
                    'email':request.form.get('email'),
                    'password':hashed,
                    'avatar': 'static/' + 'images/' + avatar + '.png',
                    'username':f'Anonymous {avatar}'
                }
                # print(user)
                users.insert_one(user)
                session['email']=request.form['email']
                user_obj= users.find_one({'email': session['email']})

                print(user_obj)
                return render_template('home.html', user=user_obj, posts=post)

        elif form_name == 'form2':
            email = request.form.get('email')
            password = request.form.get('password')

            email_found = users.find_one({'email': email})

            if email_found:
                email_val = email_found['email']
                password_check = email_found['password']
                if bcrypt.checkpw(password.encode('utf-8'), password_check):
                    session['email']=email_val
                    user_obj= users.find_one({'email': session['email']})
                    return render_template('home.html', user=user_obj, posts=post)
                else:
                    message = 'Incorrect password, please try again'  
                    return render_template('index.html', message=message)
            else:
                message = 'There is no account with that email. Please create a new account'
                return render_template('index.html', message=message)

@app.route('/logout')
def logout():
    session['email']=None
    return render_template('index.html')


@app.route('/home')
def home():
    user_obj= users.find_one({'email': session['email']})
    post=posts.find()
    print(post)
    return render_template('home.html', user=user_obj, posts=post)



@app.route('/<user_id>/home', methods=['POST'])
def post(user_id):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user_obj= users.find_one({'email': session['email']})
    avatar = user_obj['avatar']
    print(avatar)
    post = {
        'user_id':user_id,
        'user_avatar':avatar,
        'created_at':dt_string,
        'content':request.form.get('content')
    }
    posts.insert_one(post)
    print(post)
    return redirect(url_for('home', user=user_obj))


if __name__ == '__main__':
    app.run(debug=True, port=5002)