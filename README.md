Seahorse v0.5-dev
----------------
Seahorse is a fullstack asynchronous web server.  It is built with speed, realtime behavior and scalability in mind.  RethinkDB is capable of pushing changes to the Seahorse web app when data is changed.  Seahorse can notify clients through a data sync websocket.  Frontend uses React.js to take advantage of the excellent virtual dom manipulation.

Seahorse is in active development.  Its organization and design is influenced heavily by Django, Flask, and Tornado frameworks.  The goal of Seahorse is to provide a rock solid starter template and design for building asynchronous web applications.

Seahorse makes some decisions for you, like it is using RethinkDB by default for the database.  RethinkDB is a NoSQL based database with an emphasis on being asynchronous, scalable and works great with Tornado.  A more customizable design is planned, but not a high priority.



##Features
+ User Registration, Login and Logout
+ Email Backend and Verification
    - Email verification uses tokens signed generated using the config secret key and a timestamp.  This allows us to verify user email addresses without taking up any space in a database.  Also, it allows us to have a builtin timestamp for the email check.  By default the expiration is 24 hours.
+ Password Reset and Password Change Handlers
+ Password encryption
+ A synchronous application shell
+ Custom RethinkService class to easily interact with RethinkDB either synchronously or asynchronously.

+ JSX pre-compile
+ JSX directory monitoring development server autoreload
+ Decent initial logging setup

+ A markdown-based blog

+ Nose testing
+ Built on the latest Python, Tornado, RethinkDB and React libraries
+ Bower frontend package management
+ Websocket support and configuration for nGinx and dokku deployment


+ Dokku Docker Deployment
    - Necessary Dokku Plugins: 
        + dokku-apt - used to inject nodejs for React.js pre-compile. [dokku-apt](https://github.com/F4-Group/dokku-apt)
        + dokku-rethinkdb-plugin - used to install rethinkdb and link. [dokku-rethinkdb-plugin using latest RethinkDB 2.0.4](https://github.com/iepathos/dokku-rethinkdb-plugin) - waiting for updates to pull through to official dokku-rethinkdb-plugin repo.

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
+ RethinkDB 2.0.4
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



#Routes
Modules in Seahorse have their routes collected in a routes.py file.
This is done to help enforce modular design and make it extremely easy
to locate and adjust all of a module's active routes.

The base seahorse/routes.py contains the initial Index route and
serves as the central location for connecting and disconnecting modules
with the main server application.

##Default Routes
###Auth
+ /register/
+ /verify/{code}
+ /login/
+ /logout/
+ /change/password/
+ /reset/password/

###Blog
+ /blog/
+ /blog/{slug}





##Commands
````bash
Seahorse Asynchronous Web Server

optional arguments:
  -h, --help            show this help message and exit
  -r, --run             Runs the server.
  --build_tables        Build RethinkDB tables.
  -jsx, --jsx_compile   Compile JSX static files into JS files
  -s, --shell           Open an application shell.
  --add_user [ADD_USER [ADD_USER ...]]
                        Add a user to the database. Expects id and raw
                        password.
  --delete_user [DELETE_USER [DELETE_USER ...]]
                        Delete a user from the database. Expects id.
  --activate_user [ACTIVATE_USER [ACTIVATE_USER ...]]
                        Activate a user account. Expects id.
````