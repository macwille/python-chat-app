# Chat app - [DEMO](https://chat404-web.herokuapp.com)

[![License: CC0-1.0](https://licensebuttons.net/l/zero/1.0/80x15.png)](http://creativecommons.org/publicdomain/zero/1.0/)

Website where users can send messages inside chat rooms, the rooms are are divided into subjects. Once logged in the users can create new subjects and rooms, created subjects can be set to private with a password log in.

Writen in Python, using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [PostgreSQL](https://www.postgresql.org/).

You can try out the website by registering or try the admin user:

username: `Admin` password: `1234`.

## Features

* Information is saved to a database

* Registration and login.

* User can create subjects and rooms.

* User can send and delete his/her messages.

* User can create a password protected private subjects.

* Admin user.

* Website is protected against SQL injections, XSS and CSRF attacks.

### Admin User

* Has access to all rooms and subjects.

* Can delete any room or message.

* Can search all messages.

## Left Out

* Can edit messages, rooms, userinfo and subjects.

* Check inputs with regex.

* Grid list contain more info.

* User / Admin page.

* Limit number of subjects and rooms per user.

## Command Prompts

After navigating to the project folder, first steps when loading is to set up virtual enviroment to hold the project and loading dependencies.

If the command `pip install -r requirements.txt` doesn't work correctly you will need to to manually download required modules using `pip install module-name`. 

You can check all used modules from the `requirements.txt` file.

### Enviroment

To run the program localy you must create a `.env` file inside your project folder. The file will need to have the following information.

* `DATABASE_URL=postgresql://'user':'password'localhost:'PORT'/'database-name'`.

* `SECRET_KEY='generated_password'` - this information needs to be limited to local machine. 


### Linux & macOS

* `python3 -m venv venv` - Creates a local  virtual envirnoment for the project with a name 'venv'.

* `. venv/bin/activate` - Activates the virtual envirnoment.

* **(venv)** `pip install -r requirements.txt` - Checks and downloads the project dependencies.

* **(venv)** `flask run` - Runs the program on port `localhost:5000`.

### Windows

* `py -3 -m venv venv` - Creates local python 3 virtual envirnoment folder named 'venv'.

* `venv\Scripts\activate` - Activates the virtual envirnoment.

* **(venv)** `pip install -r requirements.txt` - installs dependecies.

* **(venv)** `flask run` - Starts the app on a development server (uses port 5000) defined in app.py.

### PostgreSQL

If you have [PostgreSQL](https://www.postgresql.org/) installed you can run these commands, you will need to create a database inside your cluster.


* `DATABASE_URL=postgresql://'user:password'@localhost:'PORT'/'database-name'` - template for .env configuration.

* `psql -U 'user' -d 'database-name' < schema.sql` Creates SQL-tables.

* `psql -U 'user/superuser' -d 'database-name' < drop.sql` Deletes all SQL-tables.

