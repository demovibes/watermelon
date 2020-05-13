# watermelon
Next-generation web backend for streaming community radio, based on Django 2.2.

## Getting Started
watermelon requires several Python packages to do its job, but fortunately most
can be bootstrapped from the source distribution.  At a minimum, all you need
is a working Python 3.5+ installation - this is the oldest version supported by
Django 2.2.

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

    Watermelon now includes initial data migrations to bootstrap the service.
    An "admin" superuser with password "password" is created at first migration.
    **Change this password before going live with the site** or you will be
    sorry.

5. Launch the development server.  From the root folder, run this command:
    `python manage.py runserver`
    This will start a local webserver for testing watermelon, running at
    http://127.0.0.1:8000/.  (To run an server that can be accessed externally,
    add an IP and port, as in `python manage.py runserver 0:8080`)
    Note that the Icecast default port is 8000, so the dev server should be run
    on a different port.

## Setting up a Streamer
Once you have watermelon up it is time to set up a streamer to actually play music.
This example will use icecast + ices to run the backend.

The general idea is:

    django -----> DB
      ^
      |
    link-ices.py -> ices -> icecast
      |              ^
      v              |
     sox  -----------/

icecast is the streaming server, which accepts a source input, and allows
external clients to connect to it for broadcast listening.  ices is a "source"
which can read .ogg files and forward them to icecast.

Configure ices using a "playlist" source of type "script" and give it the path
to `contrib/link-ices.py`.  Whenever ices is ready for another song, it will
call the script, and expects to receive the name of a file to play.

The magic of queue management then happens within `link-ices.py`, which is
responsible for:
* retrieving the next item from the playlist model,
* calling SoX to convert to a .ogg file in a temp location,
* writing the metadata info to the location expected by IceS, and
* returning the temp filename to IceS for streaming.

Look into the `playlist` app for more information on how the queue works.
