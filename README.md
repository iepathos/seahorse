Seahorse v0.4-dev
----------------
Seahorse is a fullstack asynchronous web server.  It is built with speed, realtime behavior and scalability in mind.

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

Clone repo, install dependencies, start RethinkDB
````bash
cd .virtualenvs
pyenv project_name
cd ~
git clone https://github.com/iepathos/seahorse.git project_name
cd project_name
workon project_name
pip install -r requirements.txt
bower install
rethinkdb &
./seahorse.py --run
````