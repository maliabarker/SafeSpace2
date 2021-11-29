from flask import Flask, render_template, request, session
from flask_pymongo import pymongo

CONNECTION_STRING = 'mongodb+srv://maliabarker:tpofbawf@safespace.8qywl.mongodb.net/safespace?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_default_database()
users = db.users

app = Flask(__name__)

@app.route('/')
def index():
    """Return Landing Page"""
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        session['username']=request.form['username']
        return render_template('home-page.html')
    elif request.method=='POST':
        user = {
            'email':request.form.get('email'),
            'password':request.form.get('password'),
            'avatar':request.form.get('avatar')
            # 'username':f'Anonymous {avatar_name}'
        }

if __name__ == '__main__':
    app.run(debug=True, port=5002)