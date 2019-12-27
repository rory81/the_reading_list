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

