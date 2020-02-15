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


@app.route('/get_books/<limit>/<offset>', methods=['GET'])
def get_books(limit, offset):
    next_page = int(offset)
    if request.args.get('genre_name'):
        upper_limit = mongo.db.books.find(
            {'genre_name': request.args.get('genre_name')}).count()
        results = mongo.db.books.find(
            {'genre_name': request.args.get('genre_name')}).sort('author').skip(int(offset)).limit(int(limit))
    else:
        upper_limit = mongo.db.books.count()
        results = mongo.db.books.find().sort('author').skip(int(offset)).limit(int(limit))
    if (int(offset)+int(limit)) < int(upper_limit):
        next_page = int(offset)+int(limit)
    if (int(offset)-int(limit)) > 0:
        prv_page = int(offset)-int(limit)
    else:
        prv_page = 0
    return render_template('books.html',
                           limit=limit,
                           offset=offset,
                           page_limit=int(offset)+int(limit),
                           first_page_limit=int(offset)-int(limit),
                           sum_books=int(upper_limit),
                           results=results,
                           next_page=next_page,
                           prv_page=prv_page,
                           genres=list(mongo.db.genres.find()))


@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    if 'user' not in session:
        flash('You have to be logged in to edit a book')
        return redirect(url_for('login'))
    else:
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
            'picture': request.form.get('picture'),
            'rating': request.form.get('rating'),
            'user_id': mongo.db.users.find_one(
                {'email': session.get('user')})['_id']
        }
    )
    return redirect(url_for('profile',
                            limit=5,
                            offset=0,
                            user=mongo.db.users.find_one({'email': session['user']})['email']))


@app.route('/add_book')
def add_book():
    if 'user' not in session:
        flash('You have to be logged in to add a book')
        return redirect(url_for('login'))
    else:
        return render_template('addbook.html', books=mongo.db.books.find(),
                               genres=mongo.db.genres.find())


@app.route('/insert_book', methods=['GET', 'POST'])
def insert_book():
    books = mongo.db.books
    new_book = request.form.to_dict()
    new_book['user_id'] = mongo.db.users.find_one(
        {'email': session.get('user')})['_id']
    books.insert_one(new_book)
    return redirect(url_for('profile',
                            limit=5,
                            offset=0,
                            user=mongo.db.users.find_one({'email': session['user']})['email']))


@app.route('/book/<book_id>')
def book(book_id):
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('per_book.html', book=the_book)


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    if 'user' not in session:
        flash('You have to be logged in to delete a book')
        return redirect(url_for('login'))
    else:
        mongo.db.books.remove({'_id': ObjectId(book_id)})
        return redirect(url_for('profile',
                                limit=5,
                                offset=0,
                                user=mongo.db.users.find_one({'email': session['user']})['email']))


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
                                            limit=5,
                                            offset=0,
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
        return redirect(url_for('profile',
                                limit=5,
                                offset=0,
                                user=user_in_db['email']))
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
            return redirect(url_for('profile',
                                    limit=5,
                                    offset=0,
                                    user=user_in_db['email']))
        else:
            flash('Wrong password or user name')
            return redirect(url_for('login'))
    else:
        flash('No account found with that email address.')
        return redirect(url_for('login'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'user' in session:
        flash('You are already signed in!')
        return redirect(url_for('get_books', limit=5, offset=0))
    if request.method == 'POST':
        form = request.form.to_dict()
        # Check if the password and password1 actualy match
        if form['password'] == form['password_2']:
            user = mongo.db.users.find_one({'email': form['email']})
            print(user['_id'])
            if user:
                hash_pass = generate_password_hash(form['password'])
                mongo.db.users.update_one({"_id": user['_id']}, {
                                          "$set": {"password": hash_pass}})
                return redirect(url_for('login'))
            else:
                flash('There is no account with this email address')
                return redirect(url_for('get_registered'))
        else:
            flash("Warning! Passwords don't match!")
            return redirect(url_for('reset_password'))
    return render_template('reset_password.html')


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You are logged out. Hope to see you soon!')
    return redirect(url_for('get_home'))


# Profile Page
@app.route('/profile/<limit>/<offset>/<user>')
def profile(limit, offset, user):
    # Check if user is logged in
    if 'user' in session:
        # If so get the user and pass him to template for now
        user_in_db = mongo.db.users.find_one(
            {'email': session.get('user')})
        next_page = int(offset)
        if request.args.get('genre_name'):
            upper_limit = mongo.db.books.find({'genre_name': request.args.get(
                'genre_name'), "user_id": ObjectId(user_in_db['_id'])}).count()
            results = mongo.db.books.find(
                {"user_id": ObjectId(user_in_db['_id'])})
            if upper_limit == 0:
                flash('There are no books for this genre!')
            else:
                results = mongo.db.books.find({'genre_name': request.args.get('genre_name'),
                                               "user_id": ObjectId(user_in_db['_id'])}).sort('author').skip(int(offset)).limit(int(limit))
        else:
            upper_limit = mongo.db.books.find(
                {"user_id": ObjectId(user_in_db['_id'])}).count()
            results = mongo.db.books.find({"user_id": ObjectId(user_in_db['_id'])}).sort(
                'author').skip(int(offset)).limit(int(limit))
        if (int(offset)+int(limit)) < int(upper_limit):
            next_page = int(offset)+int(limit)
        if (int(offset)-int(limit)) > 0:
            prv_page = int(offset)-int(limit)
        else:
            prv_page = 0
        return render_template('profile.html',
                               user=user_in_db,
                               offset=offset,
                               limit=limit,
                               page_limit=int(offset)+int(limit),
                               first_page_limit=int(offset)-int(limit),
                               sum_books=int(upper_limit),
                               next_page=next_page,
                               prv_page=prv_page,
                               results=results,
                               genres=list(mongo.db.genres.find()))
    else:
        flash('You must be logged in to view a profile')
        return redirect(url_for('get_home'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
