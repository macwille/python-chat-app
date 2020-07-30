# Chat app

Python / Flask web application to create chat enviroment for different users using SQL database.

## Definition

The application can perform following functions when it's finished: 

* Has chat rooms where registered users can leave messages

* Rooms are divided to subject areas and some areas can be limited to certain users

* User can create an unique username

* User can edit or delete his or her messages

* User can search for messages

* Users can create private subject areas

* Application has support for an admin user with rights to moderate all rooms and users

### Command prompts (Windows)

* `py -3 -m venv venv` - Creates local python 3 virtual enviroment folder named 'venv'.

* `venv\Scripts\activate` - Activates (venv) from the created venv folder.

* (venv) `pip install -r requirements.txt` installs dependecies dependencies.

* `flask run` - Starts the app on a development server (uses port 5000) defined in app.py.
