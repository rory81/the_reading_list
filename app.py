import os
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, \
    url_for, session, flash


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'reading_list'
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost')
app.secret_key = os.getenv('SECRET_KEY', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def get_home():
    return render_template('index.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/get_books/<limit>/<offset>', methods=['GET', 'POST'])
def get_books(limit, offset):
    books = mongo.db.books
    starting_point = list(books.find().sort('author'))
    end_point = starting_point[int(offset)]['author']
    upper_limit = books.count()
    print(upper_limit)
    if (int(offset)+int(limit)) < upper_limit:
        next_url = str(int(offset)+int(limit))
    else:
        next_url = str(upper_limit-1)
    print(next_url)
    if (int(offset)-int(limit)) > 0:
        prv_url = str(int(offset)-int(limit))
    else:
        prv_url = str(0)
    print(prv_url)
    books = books.find({'author': {'$gte': end_point}}
                       ).sort('author').limit(int(limit))
    results = mongo.db.books.find({'genre_name':
                                   request.form.get('genre_name')})
    return render_template('books.html',
                           books=books,
                           limit=limit,
                           offset=offset,
                           next_url=next_url,
                           prv_url=prv_url,
                           results=results,
                           genres=list(mongo.db.genres.find()))


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    all_genres = mongo.db.genres.find()
    return render_template('editbooks.html', book=the_book,
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
    return redirect(url_for('get_books', limit=5, offset=0))


@app.route('/add_book')
def add_book():
    return render_template('addbook.html', books=mongo.db.books.find(),
                           genres=mongo.db.genres.find())


@app.route('/insert_book', methods=['POST'])
def insert_book():
    books = mongo.db.books
    new_book = request.form.to_dict()
    new_book['user_id'] = "user_id"
    books.insert_one(request.form.to_dict())
    return redirect(url_for('get_books', limit=5, offset=0))


@app.route('/book/<book_id>')
def book(book_id):
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('per_book.html', book=the_book)


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_books', limit=5, offset=0))


@app.route('/books_per_genre', methods=['POST'])
def get_books_per_genre():
    return render_template('genres.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


@app.route('/genre/<genre_id>')
def genre(genre_id):
    the_genre = mongo.db.genres.find_one({'_id': ObjectId(genre_id)})
    return render_template('genres.html', genre=the_genre)


@app.route('/get_registered', methods=['GET', 'POST'])
def get_registered():
    # Check if user is not logged in already
    if 'user' in session:
        flash('You are already signed in!')
        return redirect(url_for('get_books', limit=5, offset=0))
    if request.method == 'POST':
        form = request.form.to_dict()
        # Check if the password and password1 actualy match
        if form['password'] == form['password_2']:
            # If so try to find the user in db
            user = mongo.db.users.find_one({'email': form['email']})
            if user:
                flash(f'{form["email"]} already exists!')
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
                    {'email': form['email']})
                if user_in_db:
                    # Log user in (add to session)
                    session['user'] = user_in_db['email']
                    return redirect(url_for('profile',
                                            user=user_in_db['email']))
                else:
                    flash('There was a problem saving your profile')
                    return redirect(url_for('get_registered'))

        else:
            flash('Warning! Passwords dont match!')
            return redirect(url_for('get_registered'))

    return render_template('register.html')


@app.route('/login', methods=['GET'])
def login():
    # Check if user is not logged in already
    if 'user' in session:
        user_in_db = mongo.db.users.find_one({'email': session['user']})
        if user_in_db:
            # If so redirect user to his profile
            flash('You are logged in already!')
            return redirect(url_for('profile', user=user_in_db['email']))
    else:
        # Render the page for user to be able to log in
        return render_template('login.html')


@app.route('/user_auth', methods=['POST'])
def user_auth():
    form = request.form.to_dict()
    user_in_db = mongo.db.users.find_one({'email': form['email']})
    # Check for user in databases
    if user_in_db:
        # If passwords match (hashed / real password)
        if check_password_hash(user_in_db['password'], form['password']):
            # Log user in (add to session)
            session['user'] = form['email']
            return redirect(url_for('profile', user=user_in_db['email']))
        else:
            flash('Wrong password or user name')
            return redirect(url_for('login'))
    else:
        flash('No account found with that email address.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You are logged out. Hope to see you soon!')
    return redirect(url_for('get_home'))


# Profile Page
@app.route('/profile/<user>')
def profile(user):
    # Check if user is logged in
    if 'user' in session:
        # If so get the user and pass him to template for now
        user_in_db = mongo.db.users.find_one({'email': user})
        return render_template('profile.html', user=user_in_db)
    else:
        flash('You must be logged in to view a profile')
        return redirect(url_for('get_home'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
