#/bin/bash
########################################################################
# clear_generated_files.sh
# Clear generated files in Django project 'helping'
########################################################################

########################################################################
# Functions
########################################################################

check_if_to_terminate() {
    if [ $1 != 0 ]; then
	echo "TERMINATING."
	exit 1
    fi
}

########################################################################

MYDIR=`pwd`/$(dirname $0)/..
echo Working at directory $MYDIR

whiptail --title "Confirmation" --yesno "Do you really want to clear all generated files in $MYDIR?" 9 70
check_if_to_terminate $?

echo Going to clear generated files.
echo; echo
cd $MYDIR
rm ./helping/db.sqlite3
rm -rv ./helping/tagiot/migrations/__pycache__
rm     ./helping/tagiot/migrations/0*.py
rm -rv ./helping/tagiot/__pycache__
rm -rv ./helping/common/__pycache__
rm -rv ./helping/helping/__pycache__
rm -rv ./helping/static/*
echo; echo
echo Finished clearing generated files.

echo; echo
whiptail --title "Confirmation" --yesno "Do you really want to regenerate everything in $MYDIR?" 9 70
check_if_to_terminate $?

echo Going to regenerate files.
echo; echo
cd $MYDIR
cd helping
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser --username admin
echo; echo
echo Finished regenerating files.

echo; echo
whiptail --title "Confirmation" --yesno "Do you really want to populate database from fixtures?" 9 70
check_if_to_terminate $?

echo Going to populate database from fixtures
echo; echo
cd $MYDIR
cd helping
ls -al tagiot/fixtures/*.json
./manage.py loaddata tagiot/fixtures/*.json
echo; echo
echo Finished populating database.

echo; echo
echo Finished regenerating everything

echo; echo
echo To start the test server: ./manage.py runserver 0.0.0.0:8000
echo Then, in the browser: http://localhost:8000/static/tagiot/index.html
