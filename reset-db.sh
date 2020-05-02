#!/bin/sh

. .venv/bin/activate

FILES="*/migrations/load_initial_data.py"
FILES_BAK="*/migrations/load_initial_data.py.bak"

# collect initial_data migrations
for f in $FILES
do
  echo "Backing up $f..."
  mv $f $f.bak
done

rm */migrations/0*.py
rm db.sqlite3
rm -rf uploads
python manage.py makemigrations

for f in $FILES_BAK
do
  d=`dirname $f`
  n=`basename $f .bak`
  echo "Restoring $f to $d/$n..."
  mv $f $d/$n
done

python manage.py migrate
