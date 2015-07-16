Seahorse v0.4-dev
----------------
Seahorse is a fullstack asynchronous web server.  It is built with speed, realtime behavior and scalability in mind.  RethinkDB is capable of pushing changes to the Seahorse web app when data is changed.  Seahorse can notify clients through a data sync websocket.  Frontend uses React.js to take advantage of the excellent virtual dom manipulation.

Seahorse is in active development and could change architecture and library choices drastically as it progresses.

##Features
+ User Registration, Login and Logout
+ Email Backend and Verification
    Email verification uses timestamps generated using the config secret key.  This allows us to verify user email addresses without taking up any space in a database.  Also, allows us to have a builtin timestamp for the email check.  By default the expiration is 24 hours.
+ Password Reset and Password Change Handlers
+ Password encryption

+ JSX pre-compile
+ Nice initial logging setup
+ Nose tests
+ Built on the latest Python, Tornado, RethinkDB and React libraries

+ Bower frontend package management

##Future Features
+ Project shell with synchronous db connection
+ Improve websocket setup, utility functions and handlers
+ Improve reactjs websocket integration
+ Setup instructions and integration with Dokku
+ Improve testing
+ Make email setup more modular



Python Libraries
----------------
+ Python 3.4.3
+ Tornado 4.2
+ RethinkDB 2.0
+ ItsDangerous 0.24
+ Passlib 1.6.2


Javascript Libraries
----------------
+ jQuery
+ React.js



Development Server Setup
----------------
Setup Python 3.4.3 virtualenv
````bash
cd .virtualenvs
pyvenv-3.4 project_name
````


Clone repo, install dependencies, start RethinkDB, run server
````bash
cd ~/Devel
git clone https://github.com/iepathos/seahorse.git project_name
cd project_name
workon project_name
pip install -r requirements.txt
bower install
rethinkdb &
./manage.py --run
````

Run tests
````bash
nose
````