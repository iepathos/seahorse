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
pyenv seahorse
cd ~
git clone https://github.com/iepathos/seahorse.git
cd seahorse
pip install -r requirements.txt
bower install
rethinkdb
````

Open another shell to start web server
````bash
cd seahorse
./mind --run
````