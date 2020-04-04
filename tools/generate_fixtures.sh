#/bin/bash
########################################################################
# generate_fixtures.sh
# Regenerate fixture files from database in Django project 'helping'
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

whiptail --title "Confirmation" --yesno "Do you really want to regenerate all fixture files?" 9 70
check_if_to_terminate $?

echo Going to regenerate fixture files.
echo; echo
cd $MYDIR
cd helping
./manage.py dumpdata --indent 2 tagiot.ProfileStatus tagiot.ContactType tagiot.NeedStatus tagiot.CapabilityStatus tagiot.TaskStatus > tagiot/fixtures/enumerations.json
./manage.py dumpdata --indent 2 tagiot.TaskType tagiot.TaskTypeExtra > tagiot/fixtures/tasktypes.json
echo; echo
echo Finished regenerating fixture files.

# End of generate_fixtures.sh
