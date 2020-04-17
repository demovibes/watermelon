# watermelon
Next-generation web backend for streaming community radio.
Django providing REST API.

## Getting Started
watermelon requires several Python packages to do its job, but fortunately most
can be bootstrapped from the source distribution.  At a minimum, all you need
is a working Python 3 installation.  These instructions assume version 3.3 or
greater.  Older versions will need to use `virtualenv` instead of `venv`.

1. Create a Python virtual environment, from which you will run watermelon.
  The purpose of the virtual environment is to allow Python to manage the
  dependencies for watermelon, without interfering with anything else on the
  system or requiring root priveleges.

  From the root watermelon/ folder, run:
  `python -m venv .venv`
  This will create a virtual environment within `.venv/`, containing copies of
  your Python system, as well as a version of `pip` that can be used to install
  additional dependencies.

2. Activate your new virtual environment.  This sets path variables so that the
  packages in your v.env are preferred over the system-wide ones.
  `source watermelon/.venv/bin/activate`
  (depending on your shell, the specific invocation differs: see
    https://docs.python.org/3/library/venv.html)

3. Install dependencies.  watermelon dependencies are managed by `pip` and
  tracked in the file `requirements.txt`.  You should be able to install them
  into your virtual environment in one pass with this command from the root
  folder:
  `pip install -r requirements.txt`

4. Set up the initial (empty) database.  Eventually, watermelon will ship with
  "migrations" that allow upgrade from version to version.  Because this is
  early development, migrations are not being added to version control.  You
  will need to create and apply the initial migrations from scratch:
  `python manage.py makemigrations` and then `python manage.py migrate` will
  create the skeleton for your new DB.

5. Set up an Admin user.  If this is your first time launching watermelon, you
  need an admin user with the power to create other objects.  Run this:
  `python manage.py createsuperuser`

6. Launch the development server.  From the root folder, run this command:
  `python manage.py runserver`
  This will start a local webserver for testing watermelon, running at
  http://127.0.0.1:8000/.  (To run an server that can be accessed externally,
  add an IP and port, as in `python manage.py runserver 0:8000`)
