# Chat app - [Demo](https://chat404-web.herokuapp.com)

## Demo

**try out as an admin user - username: `Admin` password: `1234` or register**

Chat room website where users can send an read messages, divided into different subjects and rooms.

Writen in Python, using Flask and PostgreSQL.

If you want to run the website locally you will need to have PostgreSQL installed.


## Features

* Information saved to Database

* Registration and login

* User can create rooms and subjects

* Send and delete messages

* User can create password restricted subjects

* Admin user

* Protected against SQL injections, XSS and CSFR attacks

### Admin user

* Has access to all rooms and subjects

* Can delete any room or message

* Can search all messages

## Possible Future Ideas

* Can edit messages, rooms and subjects

* User can edit his/her info

* Better stylesheet

## Command prompts

After navigating to the project folder, first steps when loading is to set up virtual enviroment to hold the project and loading dependencies.

If the command `pip install -r requirements.txt` doesn't work correctly you will need to to manually download required modules using `pip install module-name`. 

You can check all used modules from the `requirements.txt` file.

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

If you have PostgreSQL installed you can run these commands, you will need to create a database inside your cluster.


* `DATABASE_URL=postgresql://user:password@localhost:PORT/database-name` - template for .env configuration.

* `psql -U user/superuser -d database-name < schema.sql` Creates SQL-tables.

* `psql -U user/superuser -d database-name < drop.sql` Deletes all SQL-tables.

