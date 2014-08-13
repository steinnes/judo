judo-events
===========

This is the source code for the judo-events system.

This is a little website designed to help local coaches and trainers find
tournaments and judo-related events such as training camps and conferences
all around the world.

It is relatively easy to find details online about the larger tournaments
for the older, more professional judokas, but the smaller events, especially
children's or teenager's events are often hard to find.

Judo.Events fixes that.

It is our sincere hope that coaches around the world will appreciate this
effort and add their own local data to the database, for the betterment of
all young judokas, and advancement of the sport in general.

Setup
=====

To setup the project the following steps need to be run. 

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py popdb
```

To save time there is also the "bootstrap" make target which does the same.

Running
=======

To run the application you can simply run index.py:

```
$ python index.py
```

This will spawn a local dev server on port 5000. 
To run in production you can use uwsgi or gunicorn and simply point the wsgi
server to import app from index.

Management
==========

Maintenance / Setup commands are contained in manage.py, currently the
supported commands are:

```
Usage: manage.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create_test_events  Creates two test events, useful for UI...
  initdb              Create the database tables
  popdb               Populate the database with countries and a...
  rebuild_countries   Rebuilds the countries in the country...
  showsql             Outputs the SQL schema (table structure) as...
```
