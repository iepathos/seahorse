Seahorse v0.4-dev
----------------
Seahorse is a fullstack asynchronous web server.  It is built with speed, realtime behavior and scalability in mind.  RethinkDB is capable of pushing changes to the Seahorse web app when data is changed.  Seahorse can notify clients through a data sync websocket.  Frontend uses React.js on the frontend, taking advantage of the excellent virtual dom manipulation.

Seahorse is in active development and could change architecture and library choices drastically as it progresses.

Built with Python 3.4.3

Python Libraries
----------------
+ Tornado
+ RethinkDB
+ ItsDangerous
+ Passlib


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
./seahorse.py --run
````