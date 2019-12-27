[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/rory81/the_reading_list) 

# The Reading List


## Technologies Used


### Template Code Institute
The template provided by Code Institute is used as basis (https://github.com/Code-Institute-Org/gitpod-database-config)
and with that a repository was created on GitHub.

### MongoDB
When logged on to MongoDB Atlas (<link>, registration needed) clicking on collections will give
the option to create a new database. For this project the reading_list database was created.

Next to the newly created database is a plus-button or a trash can button. The latter is obviously to delete the database.
The former is to add collections to the database. For this project the underlined collections were made:
1. books: all books added by the users are collected here
2. genres: default genres are maintained in this collection
3. users: user info is collected when a user registers and is used to personalise the reading list
4. user_book_rating: the number of users that has rated a certain book is collected to calculate the average rating for this book

Create an instance of PyMongo and add the app into that by adding "mongo = PyMongo(app)" to the python file.


### Flask
Flask was installed by using pip3 install flask. For python 3 use pip3 and not pip.
(gitpod doesn't need the addition of sudo, but if you are working on a different IDE the command sudo pip3 install flask is probably needed)
Add the following to the app.py file: from flask import Flask

create a Flask app by adding 'app = Flask(__name__)' to the python file

### Connect Flask to MongoDB
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
6. Stop and restart the workspace





### Deployment on Heroku
When logged on to Heroku (<link>, registration needed) click the button 'New' and select the option 'Create new app'.
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
Flask==1.1.1
itsdangerous==1.1.0
Werkzeug==0.16.0

2. Procfile (note that there isn't an extension) : the Procfile is an instruction to Heroku as to which file is used as our entry point at the application.
In other words, which file is used to call the application and run it. To create a Procfile enter 'echo web: python app.py > Procfile'.
A file is created which contains the content: 'web: python app.py'.

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

Now that it is all setup click the button 'Open app' and the app is deployed.



### Acknowledgements
For the basic setup of the environment of the app and its documentation the video's from Code Institute were used "Putting The Basics in Place" (Mini Project)
and the Heroku site for a more detailed explanation of some terminology used by Heroku.