# Chat app - [Demo](https://chat404-web.herokuapp.com)

## Demo

**try out as an admin user - username: `Admin` password: `1234` or register**

Python website using Flask framework and PostgreSQL.

Web-based chat room application where users can register and chat inside different subjects and rooms.

## Current Features

* Database support

* User can register and log in with same account.

* User can send messages

* User can search for his/her messages

* Can create rooms

* User can delete his/her messages

* User can create resricted subjects

* Admin user

### Admin user can

* Enter any subject or room

* Delete any room or message

* Search for any messages

## Coming Features

* CSRF tokens

## Possible Future Ideas

* Can edit messages, rooms and subjects

* User can edit his/her info

* Better stylesheet

## Command prompts

After navigating to the project folder, first steps when loading is to set up virtual enviroment to hold the project and loading dependencies.

### Linux

* `python3 -m venv venv` - Creates a local  virtual envirnoment for the project with a name 'venv'.

* `source venv/bin/activate` - Activates the virtual envirnoment.

* **(venv)** `pip install -r requirements.txt` - Checks and downloads the project dependencies.

* **(venv)** `flask run` - Runs the program on port `localhost:5000`.

### Windows

* `py -3 -m venv venv` - Creates local python 3 virtual envirnoment folder named 'venv'.

* `venv\Scripts\activate` - Activates virtual envirnoment.

* **(venv)** `pip install -r requirements.txt` - installs dependecies.

* **(venv)** `flask run` - Starts the app on a development server (uses port 5000) defined in app.py.


### PostgreSQL

If you have PostgreSQL installed you can run these commands.


* `DATABASE_URL=postgresql://user:password@localhost:PORT/database` - template for .env configuration.

* `psql -U user/superuser -d database < schema.sql` Creates SQL-tables.

* `psql -U user/superuser -d database < drop.sql` Deletes all SQL-tables.

