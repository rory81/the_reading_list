[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/rory81/the_reading_list) 

<img src="{{url_for('static', filename='images/tree_with_books_small.png')}}">

# The Reading List
###### Disclaimer: *this app is made for educational use only.*
The current book apps have a lot of commercials, all books have many genres making it impossible to get an idea about what the book is really about.
The books that get automatically chosen are the books with the highest rating, eventhough those do not necesarily are the best books.
It is like the movies, when there are a lot of famous actors or have won many oscars the changes are high that I am not going to like the movie.

So The Reading List should be like just like a library, see what is available and add it to your own list where you can give it your own rating and description.
The user can see what other books are added by other users and use the link to buy the book if the book looks interesting.

## UX, features for now and in the future
Before going into the user stories it should be noted that a future feature should be to connect to an excisting database of books.
That way the user doesn't have to fill in the books manually. But for now it is a good way to implement the C (create) from the CRUD principle.


### **Home**
They say don't judge a book by its cover, but there are readers that pick a book based on how pretty, weird or scary the cover looks.
The home page triggers that visual aspect by displaying a set of book covers. But eventhough the cover is important the mood of a reader determines what genre the book is going to be.
For that reason the covers are grouped per genre and the user can click on a cover to read the book description or see the authors name.
The books in the database are ordered by id's in descending order, so new books will be shown on the homepage.
If the reader has made a choice which genre it is going to be, but the books on the home page didn't peak its interest there is a link underneath the book covers to show all books in the database with that genre.

For easy redirect to the homepage the tree logo as well as the "The Reading List" title can lead the user to back to the home page.
This is especially relevant when using small devices and the navigation is a hamburger menu which needs an additional click.


### **All books**
These books can be scrolled through even if you aren't a user yet, so they can get inspiration about what they could possibly want to add if or when they create an account. 
The books in the database are ordered by id's in descending order, so new books will be easily detected.
When the books cover or title is clicked it will be redirected to the books page, but will not give the edit and delete button to prevent a user to delete/edit a book from another user.
This option is however available when the user logs in and selects a book from its profile page.
The smaller devices have a dropdown to choose books of a particular genre and the larger devices will have a sidenavigation instead to choose the genre of interest.
Pagination of 5 books per page will make it readible and the next or previous cursor will disappear when there are no more books or when the first page is reached.

The All books and Home page are the R (read) from the CRUD principle.


### **Add a book**
A future feature will be that the user doesn't have to add all books manually, because it is a tedious job. The new feature should include a connection to an excisting database to select from, 
but also the ability to add a book that was added by another user. Therefore, a book should be able to obtain more than one user_id.
Known bug is that a book can be entered twice by different users and then will be displayed twice in the all books page. This will solved with the previous mentioned feature.

A book can only be added when you have an account, therefore if no user is logged on and clicks this tab the reader will be redirected to the login page with a flash message accordingly.
Do to the limited time for the setup of this project a selected number of field are implemented with a specific goal:

#### *Book Title & Author*:
These are the obvious specifics for a book as a user might like a specific author or only knows a title and not the author from the grapevine. 

#### *Book Genre*:
As stated before the genre can be important, because the mood of a reader can determine what genre the reader would like to read.
This could be to cheer them up, their ready for an escape from reality or in need of some romance.
Sometimes more choose isn't always better, therefore a dropdown with just 6 genres forces the reader to really think about the book and choose the genre best suited. 

#### *Book Series*:
When the description graps the readers interests in a way that they want to buy it instantly, it is nice to know that the desciption is for book 5 from a serie.
Although it isn't always the case with book series, the reader might want to start with the first book not the fifth. A reader would like to know this before he buys volume 5 of the series.

#### *Published*:
Some readers are more interested in the latest books and will instantly skip books that are published longer than say a year ago.
The datepicker should make it a little bit easier to fill in the form manually while anxiously awaiting the connection to a database.

#### *Amazon link*:
It says Amazon link as the new feature will be most likely a connection to Amazon as it serves a dual purpose as you can buy books there too.
The latter is important, because when the new volume of your favorite series drops you want to buy it instantly.
This is also the case when you are bored and you have a Kindle account, so you can be redirected to the amazon site to get your book through Kindle.

#### *Book Description*:
The book desciption will be short but can hook other readers to read/buy this book. 
At least the user can give its own description and its own interpretation to the book.

#### *Picture*:
Not only for the readers that are more visually inspired to choose a book, but also for the readers who saw the book at someones desk at the office.
They usually do not remember the title nor the author, but when they see the cover they instantly remember that that was the book on the desk. 

#### *Rating*:
A personal rating from a user. When the new feature is implemented that a book can be added by multiple users in a more simpler way, this rating needs to become an average.
Important when implementing that new feature is that the personal rating is also saved.
The rating is important for the readers that are only interested in the books that rank highest and instantly ignore the books lower than 4 stars.

When the form is filled in and is submitted the user_id from the reader logged into the app will also be submitted and added to the database.
Adding these fields to the database is the C (create) from the CRUD principle.


### **My Books**
My Books is the profile page for the user. The setup is identical to the "All Books" page, but with a few differences
- If the user isn't logged on and clicks this tab it will redirect to the login page with the flash message that login is required to go to the profile page.
- Only the books that were added by the user that is logged in will be shown.
- When a specific book is clicked it will be directed to the book page, but now it has the edit and the delete option.

#### *Edit button*
The edit button will direct the user to the same form that is used to add a book, only now the previously entered values are prefilled in the form.
All fields can be updated and are submitted by the update button on the form. The user might want to adjust the description or rating or has errored in filling in the form.

Updating the altered fields in the database is the U (update) from the CRUD principle

#### *Delete button*
Sometimes a book can disappoint or a reader can change its mind. Therefore a delete button is made.
To make sure the button is not clicked by accident a confirmation message will appear. Only after confirmation will the book be deleted.

Deleting the book from the database is the D (delete) from the CRUD principle

### **Register, Login & Logout**
The Register form is used to create an account. There is a check to see if a user is already logged on or if the entered email address is already in use.
Password needs to be entered twice to make sure there are no typo's and will be saved as a hash to the database.
When the user is on the register page, but already has an account there is a link available to redirect to the login page.

When Login is chosen and the user is already logged in than the user will be redirected to its profile page. The user can forget its password, because lets be honest you need to remember so many passwords nowadays. 
Therefore a reset password link is added. Updating the (hashed) password is the U (update) from the CRUD principle.

The Logout option states the obvious and will make sure the profile from that user is no longer available without having to log in again.



## Technologies Used
- [Template Code Institute](https://github.com/Code-Institute-Org/gitpod-database-config) : basic installation to be able to use libraries and flask and python
- [MongoDB](https://www.mongodb.com/) - registration needed: used for database
- [Flask](https://flask.palletsprojects.com/en/1.1.x/): to make routes and reroutes to dynamically setup the website
- [Python3](https://www.python.org/download/releases/3.0/): to program the flask elements to accommodate the user stories
- [Materialize](https://materializecss.com/): use styling elements like a the form or dropdown that are easier to implement with materialize
- [Bootstrap](https://getbootstrap.com/): using styling elements like grids or classes or buttons to style the page
- [Jquery](https://jquery.com/): used to initialize madterialize elements
- [Javascript](https://www.javascript.com/): used for instance for the implementation of the star rating.
- [Gitpod](https://www.gitpod.io/): used as IDE
- [Heroku](https://www.heroku.com/): used as deployment platform

Imported for use in the Reading List app:
- import os: standard python library
- werkzeug.security (import generate_password_hash, check_password_hash): to hash the password and reverse it so it can be checked with the entered value.
- bson.objectid (import ObjectId): to be able to read and write to and from the mongodb database by using the same format
- flask_pymongo (import PyMongo) : so that mongo can communicate with python
- flask (import Flask, render_template, redirect, request, url_for, session, flash) : to use the options that flask gives like seeing if a user is in session or to reroute when necessary.


### **Template Code Institute**
The template provided by Code Institute is used as basis (https://github.com/Code-Institute-Org/gitpod-database-config)
and with that a repository was created on GitHub.


### **MongoDB**
When logged on to MongoDB (https://www.mongodb.com/, registration needed) clicking on collections will give
the option to create a new database. For this project the reading_list database was created.

Next to the newly created database is a plus-button or a trash can button. The latter is obviously to delete the database.
The former is to add collections to the database. For this project the underlined collections were made:
1. books: all books added by the users are collected here, with the user_id from the user who added the book
2. genres: default genres are maintained in this collection
3. users: user info is collected when a user registers and is used to personalise the reading list

Create an instance of PyMongo and add the app into that by adding "mongo = PyMongo(app)" to the python file.


### **Flask**
Flask was installed by using pip3 install flask. For python 3 use pip3 and not pip.
(gitpod doesn't need the addition of sudo, but if you are working on a different IDE the command sudo pip3 install flask is probably needed)
Add the following to the app.py file: from flask import Flask

create a Flask app by adding 'app = Flask(__name__)' to the python file

### **Connect Flask to MongoDB**
To get Flask talking to MongoDB a third party library needs to be installed by entering 'pip3 install flask-pymongo' in the terminal.
Additionally, a package called dnspython needs to be installed to be able to connect to MongoDB Atlas. Use the command 'pip3 install dnspython'.

Add the underlining to the app.py file:

---to be able to access the library---
from flask_pymongo import PyMongo

---the data stored in MongoDB is in the BSON-format, so access to the BSON-library is needed---
from bson.objectid import objectid

Now that the libraries are in place we need to add the underlining configuration to this Flask application in the python file:

app.config["MONGO_DBNAME"] = 'the-reading-list'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

The "MONGO_URI" is a link that is provided by MongoDB:
1. Go to MongoDB en select "Overview"
2. On the right click the Connect-button
3. In the pop-up choose the option "Connect Your Application"
4. Copy the provided link with the format: mongodb+srv://rory81:<password>@myfirstcluster-nn45a.mongodb.net/<name_database>?retryWrites=true&w=majority
    a) change <password> to your own personal password
    b) change <name_database> to 'the_reading_list'
5. Use https://gitpod.io/environment-variables/ to set MONGO_URI as an environment variable
    a) Name= MONGO_URI
    b) Value= the link from step 4 with the correct password and database name
    c) repository= the workspace directory
6. Use https://gitpod.io/environment-variables/ to set SECRET_KEY as an environment variable, needed to encode the session cookie
    (used to see if a user is already logged in or not) 
    a) Name= SECRET_KEY
    b) Value= make it as complex as possible
    c) repository= the workspace directory
7. Stop and restart the workspace


## Git(Hub) version control
Git is used to track the changes made and with that to have version control. The following steps are needed to track the changes made in the local repository:

**Step 1: $ git add [file]** Snapshots the file in preparation for versioning. For [file] fill in the (path to the) filename to be versioned.

**Step 2: $ git commit -m "[descriptive message]"** Records file snapshots permanently in version history. In the descriptive message a short description of the changes made are stated.

**Step 3: $ git push [file]** Uploads the local commits to GitHub

Branches where created to experiment with new features by using:
**Step 1: $ git branch [branch name]** To create the branch
**Step 2: $ git checkout [branch name]** To go to that branch to work on and the previous steps to add, commit and push applies.

After the work on the branch is deemed good enough to be deployed it will be merged tot the master branch:
**Step 1: $ git checkout master** To go to the master branch
**Step 2: $ git merge [branch name]** To merge the branch into the master branch

## Deployment on Heroku
When logged on to Heroku (https://www.heroku.com/, registration needed) click the button 'New' and select the option 'Create new app'.
Give the app a name, but be aware that this should be an unique name and not previously used by you or another app on heroku.

Choose region closest by you, because then Heroku will select the edge server that is in that region, making the delivery a bit quicker.
In this case Europe was choosen.

To login to Heroku on the IDE enter 'heroku login' in the terminal and enter your credentials as requested.
However, this will not work on Gitpod. Enter 'heroku login -i' instead and enter your credentials as requested.

By login to Heroku in the IDE a connection is created between the application in the IDE and Heroku 
that would allow to push changes (using Git) to update the application at any given time.

To check if the newly created app is connected enter 'heroku apps' in the terminal. Underneath your e-mail address a list of apps will be listed.
For this particular app 'the-reading-list (eu)' is shown.

As we have already created a Git repository by using the Code Institute template, 
the next step is to add the files needed for this app to the repository by entering:
1. '$ git add .' in the terminal,
2. followed by a '$ git commit -m "message of choice"'

To associate the Heroku app as the master branch enter:
$ heroku git:remote -a the-reading_list

When you push to Heroku at this point it will fail, because two additional files are needed to succesfully deploy to Heroku:
1. requirements.txt : the requirements text file will contain a list of the application that are required for Heroku to run the application.
To create this file enter 'pip3 freeze --local>requirements.txt' in the terminal. A file is then generated and contains the underlining content:

Click==7.0
dnspython==1.16.0
Flask==1.1.1
Flask-PyMongo==2.3.0
itsdangerous==1.1.0
pymongo==3.10.0
Werkzeug==0.16.0

2. Procfile (note that there isn't an extension) : the Procfile is an instruction to Heroku as to which file is used as our entry point at the application.
In other words, which file is used to call the application and run it. To create a Procfile enter 'echo web: python app.py > Procfile'.
A file is created which contains the content: 'web: python3 app.py'.

Do not forget to add the two files to GitHub, using the previously mentioned git add and git commit.

Now that all files are in place the content can be pushed to Heroku by entering 'git push heroku master' to the terminal.
To run the application with Heroku enter 'heroku ps:scale web=1' to the terminal. 

For the free version only one dyno can be used. 
Dynos are isolated, virtualized Linux containers that are designed to execute code based on a user-specified command.
In this case the web dyno is used. Web dynos are of the "web" process type that is defined in the previously generated Procfile. Only web dynos recieve HTTP traffic from routers.

When this command has run succesfully the sentence 'Scaling dynos... done, now running web at 1:Free' will appear.

The only thing left to do is to specify the IP and port by adding them as configuration variables in Heroku.
1. Login to Heroku and go to the app
2. select the Settings button from the navigation
3. Go to the section 'Config Vars' and click the Add-button
    a. set the Key to 'IP'. Set the value of IP to 0.0.0.0
    b. set the Key to 'PORT'. Set the value of PORT to 5000
    c. set the Key to 'MONGO_URI'. Set the value to mongodb+srv://rory81:<password>@myfirstcluster-nn45a.mongodb.net/<name_database>?retryWrites=true&w=majority

Now that it is all setup click the button 'Open app' and the app is deployed.
If a "404 Not Found" appears it is probably due to a missing @app.route('/'). After @app.route('/') come the routes needed to make this website work.

## Run Locally
To run locally, this repository can be cloned directly into the editor of your choice by pasting git clone  into your terminal. To cut ties with this GitHub repository, type git remote rm origin into the terminal.

The underlining steps are needed to clone this GitHub repository to another local repository:

**Step 1:** navigate to the repository for this Reading List (login needed) *https://github.com/rory81/the_reading_list*

**Step 2:** click on the green button saying **Clone or download**

**Step 3:** In the Clone with HTTPs section, copy the clone URL (https://github.com/rory81/the_reading_list.git) for the repository

**Step 4:** Go to the IDE that you are using (like for instance Gitpod) and open the terminal

**Step 5:** Type `git clone [URL]`. For [URL] fill in the URL that was copied in step 3 and press Enter

## Testing
1. The pages are validated using:
[HTML validation](https://validator.w3.org/#validate_by_input): the flask elements will create an error.
Therefor the pages where run with Chrome and **CTRL+U** was used to "view page source". This source code was entered into the validator.

From this 1 warning and 1 error was detected, both of them are explainable:
- **base.html:** warning Consider avoiding viewport values that prevent users from resizing documents.
This adjustment to the viewport was needed to make the dropdown working on mobile (is a known materialize bug) and didn't see any problems with resizing
Because it is in the base.html it will occur on all pages.
- **editbook:** 1 error using select without multiple, due to working with flask and the genre in genre function where the value from the database is preselected.


The following pages where checked and ok. They were checked with the original viewport setting to be sure:
- addbook
- all books
- my books
- home 
- login
- per_book(no_edit)
- register
- reset_password

[CSS validation](https://jigsaw.w3.org/css-validator/#validate_by_input): No errors/warnings Found
[Python validation](https://extendsclass.com/python-tester.html):
Error was found because the following code was found:
**flash(f'{form["email"]} already exists)**
because this feature is only available on python 3.6 and greater. As python 2.x versions are still in use the code was rewritten to:
**flash("{} already exists!".format(form["email"]))**

2. The console was checked for errors:
- There was an error on the star rating code. This was due to the fact that the code was added to the base.html and not to the pages that actually use the star rating.
This caused an error on the pages that *didn't* used the star rating because there was no attribute to put in the code. By putting the code solely on the addbook and editbook page,
where the star rating is used, the error disappeared.

- Had a flavicon error: solved it by adding een flavicon link with the reading list logo in it
- Had a popper error when using the dropdown in the addbook or editbook page. This was due to redundant JQuery code in the base.html

3. Check forms:
- To check the addbook forms many books were manually added creating a database per genre with:

Chick Lit:   9 books
Crime:      10 books
Fantasy:    10 books
Fiction:    10 books
Music:      11 books
Mystery:     8 books

- To check the edit book forms many books were edited, including, the star rating, to see if the book was updated in the database
- To check the delete button and the confirmation window, many books were deleted (after confirmation) or attempted but pressed aborted to see if the cancelation also worked.
- 2 users were asked to create an account.
- 1 user was asked to reset password.
- validations were checked (note: email addresses without for instance **.com** are permitted due to email addresses like @edu).
Like deliberately: 
a) login with a email address unknown to database
b) login with wrong password
c) register with an email address already in database
d) register and not entering the same password twice
e) add a book with amazon link en picture not using the right format
f) check the required fields if they are really required.

4. Check pagination:
There are 5 books per page. The above mentioned number of books per genre were used to test the pagination. Some genres have exactly ten books (exactly 2 pages), 
other genres have one or two books less/more, so that standard number of 5 books per pages do no longer apply, to see if pagination still works.

5. Check genre filter:
Used a test user (email: test_case@gmail.com, password: Test1234) that has books for many genres (to test pagination), but none for 1 genre. 
Thereby testing if the redirect to profile page and the flash message work

6. Tested on multiple devices:
Used the standard dev tools from Chrome to test the different devices. Also tested it live on:
- a bigger, less standard, screen
- one user tested it on an iPad (old version) and iPhone
- tested it on a android (MIU Xiamio)
- tested it on a beamer screen during a session with 2 users.

## Acknowledgements
- For the basic setup of the environment of the app and its documentation the video's from Code Institute were used "Putting The Basics in Place" (Mini Project)
and the Heroku site for a more detailed explanation of some terminology used by Heroku.

- logo picture: https://www.kindpng.com/downpng/JRRJib_vector-knowledge-color-tree-illustration-book-reading-book/

- https://www.w3schools.com/ & https://stackoverflow.com/ to help with issues

- https://gist.github.com/prof3ssorSt3v3/29e623d441e8174ffaef17741a1bba14 (star rating system)

- https://github.com/MiroslavSvec/DCD_lead (register/login/hashing password)

- my mentor, Maranatha Ilesanmi,for challenging me and helping when needed.

- people on slack, a few in particular, who helped me when I was ready to throw in the towel.

- tutors from Code Institute for helping and sparring

- Friend of my to give me some basics for python