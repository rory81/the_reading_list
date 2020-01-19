from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import os
from flask import Flask, render_template, redirect, request, url_for, session, flash


app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'reading_list'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
app.secret_key = "super secret key"

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def get_home():
    return render_template('index.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/get_books')
def get_books():
    return render_template("books.html", books=mongo.db.books.find())


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    all_genres = mongo.db.genres.find()
    return render_template("editbooks.html", book=the_book,
                           genres=all_genres)


@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    books = mongo.db.books
    books.update(
        {'_id': ObjectId(book_id)},
        {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'genre_name': request.form.get('genre_name'),
            'series': request.form.get('series'),
            'published': request.form.get('published'),
            'amazon': request.form.get('amazon'),
            'description': request.form.get('description'),
            'picture': request.form.get('picture')
        }
    )
    return redirect(url_for('get_books'))


@app.route('/add_book')
def add_book():
    return render_template('addbook.html', books=mongo.db.books.find(),
                           genres=mongo.db.genres.find())


@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    new_book = request.form.to_dict()
    new_book['user_id'] = 'userid'
    books.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))


@app.route('/book/<book_id>')
def book(book_id):
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("per_book.html", book=the_book)


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_books'))


@app.route('/books_per_genre')
def get_books_per_genre():
    return render_template('genres.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/get_registered', methods=['GET', 'POST'])
def get_registered():
    # Check if user is not logged in already
    if 'user' in session:
        flash('You are already sign in!')
        return redirect(url_for('get_books'))
    if request.method == 'POST':
        form = request.form.to_dict()
        # Check if the password and password1 actualy match
        if form['password'] == form['password_2']:
            # If so try to find the user in db
            user = mongo.db.users.find_one({"email": form['email']})
            if user:
                flash(f"{form['email']} already exists!")
                return redirect(url_for('get_registered'))
            # If user does not exist register new user
            else:
                # Hash password
                hash_pass = generate_password_hash(form['password'])
                # Create new user with hashed password
                mongo.db.users.insert_one(
                    {
                        'first': form['first'],
                        'last': form['last'],
                        'email': form['email'],
                        'password': hash_pass
                    }
                )
                # Check if user is actualy saved
                user_in_db = mongo.db.users.find_one(
                    {"email": form['email']})
                if user_in_db:
                    # Log user in (add to session)
                    session['user'] = user_in_db['email']
                    return redirect(url_for('get_books',
                                            user=user_in_db['email']))
                else:
                    flash("There was a problem saving your profile")
                    return redirect(url_for('get_registered'))

        else:
            flash("Warning! Passwords dont match!")
            return redirect(url_for('get_registered'))

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template('login.html', users=mongo.db.users.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
