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


### Flask
Flask was installed by using pip3 install flask. For python 3 use pip3 and not pip.
(gitpod doesn't need the addition of sudo, but if you are working on a different IDE the command sudo pip3 install flask is probably needed)


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

Now that all files are in place add everything to GitHub, using the previously mentioned git add and git commit.
