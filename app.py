import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'reading_list'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_books')
def get_books():
    return render_template("books.html", books=mongo.db.books.find())


@app.route('/get_genres')
def get_genres():
    return render_template('genres.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/get_users')
def get_users():
    return render_template('users.html', users=mongo.db.users.find())


@app.route('/get_registered')
def get_registered():
    return render_template('register.html', users=mongo.db.users.find())


@app.route('/login')
def login():
    return render_template('login.html', users=mongo.db.users.find())


@app.route('/insert_user', methods=['POST'])
def insert_user():
    users = mongo.db.users
    users.insert_one(request.form.to_dict())
    return redirect(url_for('get_users'))


@app.route('/add_book')
def add_book():
    return render_template('addbook.html', books=mongo.db.books.find(),
                           genres=mongo.db.genres.find())


@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
