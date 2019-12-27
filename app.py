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
    return render_template('books.html', books=mongo.db.books.find())


@app.route('/get_genres')
def get_genres():
    return render_template('genres.html', genres=mongo.db.genres.find())


@app.route('/get_registered')
def get_registered():
    return render_template('register.html', users=mongo.db.users.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
