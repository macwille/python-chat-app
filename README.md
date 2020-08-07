# Chat app

### WORK IN PROGRESS

Flask enviroment based Python web application for running a chat room website with backend database using PostgreSQL.

## Current Features

* User can register and log in with same account.

* Rooms show messages of that room.

* App has working database.

#### Bugs

* Sending a message not working.

## Website

Project will be using [Heroku](https://dashboard.heroku.com/home) for running the website.

When website is running on Heroku server you can find it [here](https://chat404-web.herokuapp.com/), it may take some time loading for the first time.

### **Website version may be older than current code!**

## Definition

The application can perform following functions when it's finished: 

* Has chat rooms where registered users can leave messages

* Rooms are divided to subject areas and some areas can be limited to certain users

* User can create an unique username

* User can edit or delete his or her messages

* User can search for messages

* Users can create private subject areas

* Application has support for an admin user with rights to moderate all rooms and users

### Command prompts
#### Linux

* `python3 -m venv venv` - Creates local python 3 virtual enviroment folder named 'venv'. (Inside project folder)

* `source venv/bin/activate` - Activates (venv) from the created venv folder.

* (venv) `pip install -r requirements.txt` installs dependecies dependencies.

* (venv) `flask run` - Starts the app on a development server (uses port 5000) defined in app.py.

* (venv) `psql -U postgres -d chat < schema.sql` Creates SQL-tables from [schema](https://github.com/Viltska/python-chat-app/blob/master/schema.sql)

#### Windows

* `py -3 -m venv venv` - Creates local python 3 virtual enviroment folder named 'venv'. (Inside project folder)

* `venv\Scripts\activate` - Activates (venv) from the created venv folder.

*  (venv) `pip install -r requirements.txt` installs dependecies dependencies.

* (venv) `flask run` - Starts the app on a development server (uses port 5000) defined in app.py.

* (venv) `psql -U postgres -d chat < schema.sql` Creates SQL-tables from [schema](https://github.com/Viltska/python-chat-app/blob/master/schema.sql)
