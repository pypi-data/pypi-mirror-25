Medlemssys
==========

Medlemssys is a membership register.  Primarily written for norwegian youth
organizations, but can and is used by other kinds of organizations.

It doesn't do anything very advanced, but provides a way to list the members,
export to CSV, can read OCR-files, send emails and some more.

Installation
------------

Doing a simple install, you can install "medlemssys" for a test version, or
"medlemssys[production]" to get a few required extras for a real setup::

    pip install medlemssys[production]

You'll use the `medlemssys` command for all commands.  It's a small wrapper
around the django-admin command.  The first thing you'll want to do is to
create a settings file::

    medlemssys init

This will give you a `medlemssys_conf.py` file.  Have a look at it, and change
what you need.  You should load in the data to the database and create yourself
a user::

    medlemssys migrate
    medlemssys createsuperuser

If you chose the production setup, you can run gunicorn using a handy wrapper::

    medlemssys gunicorn --bind 0.0.0.0:8000

You can of course also try the django development server to just test your
register::

    medlemssys runserver 0.0.0.0:8000



