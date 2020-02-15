import os
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, \
    url_for, session, flash

# setup environment for the app
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'reading_list'
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost')
app.secret_key = os.getenv('SECRET_KEY', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
# displays the home page
@app.route('/home')
def get_home():
    return render_template('index.html', genres=mongo.db.genres.find(),
                           books=list(mongo.db.books.find()))


# displays all the books ever added by users and all books are visible to all users
# with or without an account
# limit is the number of books per page and offset is the index where to start on a certain page
@app.route('/get_books/<limit>/<offset>', methods=['GET'])
def get_books(limit, offset):
    # how to get the books for a selected genre
    if request.args.get('genre_name'):
        upper_limit = mongo.db.books.find(
            {'genre_name': request.args.get('genre_name')}).count()
        results = mongo.db.books.find(
            {'genre_name': request.args.get('genre_name')}).sort('author').skip(int(offset)).limit(int(limit))
    else:
        upper_limit = mongo.db.books.count()
        results = mongo.db.books.find().sort('author').skip(int(offset)).limit(int(limit))
    # setup pagination
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


# this route takes the user to the form that makes it possible to update/change the specifics for that particular book
@app.route('/edit_book/<book_id>')
def edit_book(book_id):
    # the book can only be updated if a user is logged on else it goes to the login page
    if 'user' not in session:
        flash('You have to be logged in to edit a book')
        return redirect(url_for('login'))
    else:
        # find the specifics of the book that was selected
        the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
        all_genres = mongo.db.genres.find()
        return render_template('editbooks.html', book=the_book,
                               genres=all_genres)


# this route will update the database based on the data that the user entered into the form from the @app.route('/edit_book/<book_id>')
@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    books = mongo.db.books
    # update the listed fields from the database
    # with the value obtained from the form that the filled in by the user in the previous route
    # but only for the book with a certain book_id
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


# because this app isn't yet linked to a database of existing books (feature for the future)
# every book a user is interested can be entered manually
# this route will give the form for the user to fill in the specifics for the book
@app.route('/add_book')
def add_book():
    # a user cannot add a book if it isn't logged on, as a user_id is registered with the book to make the profile page
    if 'user' not in session:
        flash('You have to be logged in to add a book')
        return redirect(url_for('login'))
    else:
        return render_template('addbook.html', books=mongo.db.books.find(),
                               genres=mongo.db.genres.find())


# this route will use the values entered in the form in the previous route and insert them into the database
# with those values the user_id from the user who added the book will also be added to the database
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


# books added can individually be shown by selecting the cover picture or the book title
# this route makes the buttons available to edit/update or delete a book
# only books on the profile page can be seen as that are the only books a user should be autorized to update/delete
@app.route('/book/<book_id>')
def book(book_id):
    the_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('per_book.html', book=the_book)


# this route will make it possible to delete a book from the database
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('profile',
                            limit=5,
                            offset=0,
                            user=mongo.db.users.find_one({'email': session['user']})['email']))


# this route will lead to the form for the user to enter its user data to make an account
@app.route('/get_registered', methods=['GET', 'POST'])
def get_registered():
    # Check if user is not logged in already
    if 'user' in session:
        flash('You are already signed in!')
        return redirect(url_for('get_books', limit=5, offset=0))
    if request.method == 'POST':
        form = request.form.to_dict()
        # Check if the password and password2 actualy match
        if form['password'] == form['password_2']:
            # See if the user is already in the database
            user = mongo.db.users.find_one({'email': form['email']})
            if user:
                flash("{} already exists!".format(form["email"]))
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
                    return render_template('addbook.html', books=mongo.db.books.find(),
                                           genres=mongo.db.genres.find())
                else:
                    flash('There was a problem saving your profile')
                    return redirect(url_for('get_registered'))
        else:
            flash('Warning! Passwords dont match!')
            return redirect(url_for('get_registered'))

    return render_template('register.html')


# when a user has an account it can use this route to get to the form to login to its profile page
@app.route('/login', methods=['GET'])
def login():
    # Check if user is not logged in already. If so it will redirect to the profile page
    if 'user' in session:
        user_in_db = mongo.db.users.find_one({'email': session['user']})
        return redirect(url_for('profile',
                                limit=5,
                                offset=0,
                                user=user_in_db['email']))
    else:
        # Render the page for user to be able to log in
        return render_template('login.html')


# if the user has filled in the login form, this route will autenticate the user
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


# this route will not only lead to the form to reset a password,
# but this route also makes it possible to actually update the password from the entered values in the form
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        form = request.form.to_dict()
        # Check if the user has an account for which a password can be reset
        # and to check if the new password and new password2 actualy match
        if form['password'] == form['password_2']:
            user = mongo.db.users.find_one({'email': form['email']})
            print(user)
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


# if the user wants to logout so its profile page, and the options available when logged on, are no longer accessible
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You are logged out. Hope to see you soon!')
    return redirect(url_for('get_home'))


# When a user is logged on it can make a Profile Page
# on this profile page only books added by him can be seen
# options as the single book_page, and the edit and delete functionality are available then
@app.route('/profile/<limit>/<offset>/<user>')
def profile(limit, offset, user):
    # Check if user is logged in
    if 'user' in session:
        # If so get the user
        user_in_db = mongo.db.users.find_one(
            {'email': session.get('user')})
        # setup pagination
        upper_limit = mongo.db.books.find().count()
        if (int(offset)+int(limit)) < int(upper_limit):
            next_page = int(offset)+int(limit)
        if (int(offset)-int(limit)) > 0:
            prv_page = int(offset)-int(limit)
        else:
            prv_page = 0
        # displays the books added by this user for the selected genre
        if request.args.get('genre_name'):
            upper_limit = mongo.db.books.find({'genre_name': request.args.get(
                'genre_name'), "user_id": ObjectId(user_in_db['_id'])}).count()
            results = mongo.db.books.find(
                {"user_id": ObjectId(user_in_db['_id'])})
            if upper_limit == 0:
                flash('There are no books for this genre!')
                return redirect(url_for('profile',
                                        limit=5,
                                        offset=0,
                                        user=mongo.db.users.find_one({'email': session['user']})['email']))
            else:
                results = mongo.db.books.find({'genre_name': request.args.get('genre_name'),
                                               "user_id": ObjectId(user_in_db['_id'])}).sort('author').skip(int(offset)).limit(int(limit))
        else:
            upper_limit = mongo.db.books.find(
                {"user_id": ObjectId(user_in_db['_id'])}).count()
            results = mongo.db.books.find({"user_id": ObjectId(user_in_db['_id'])}).sort(
                'author').skip(int(offset)).limit(int(limit))

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
