# Chat app - [Website](https://chat404-web.herokuapp.com)

### WORK IN PROGRESS

Flask enviroment based Python web application for running a chat room website with backend database using PostgreSQL.

## Current Features

* User can register and log in with same account.

* User can enter room and type messages.

* App has a working database

* Can search messages

* Rooms sorted by subjects

* Flash messages support

## Website

Project will be using [Heroku](https://dashboard.heroku.com/home).

When website is up and running on Heroku server you can find it [here](https://chat404-web.herokuapp.com/), it may take some time loading for the first time.

### **Website version may be older than current code!**

## Planned Features

The application can perform following functions when it's finished: 

* User can edit or delete his or her messages

* Restricted rooms checked

* User can create rooms

* Admin user

## Command prompts

After navigating to the project folder.

### Linux

* `python3 -m venv venv` - Creates local python 3 virtual envirnoment folder named 'venv'.

* `source venv/bin/activate` - Activates virtual envirnoment.

* **(venv)** `pip install -r requirements.txt` - installs dependecies

* **(venv)** `flask run` - Starts the app on a development server (uses port 5000) defined in app.py.

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

