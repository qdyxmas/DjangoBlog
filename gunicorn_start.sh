#!/bin/bash
killall -9 gunicorn
NAME="djangoblog"
DJANGODIR=/home/server/python/djangoblog #Django project directory
USER=root	# the user to run as
GROUP=root	# the group to run as
NUM_WORKERS=1 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=djangoblog.settings # which settings file should Django use
DJANGO_WSGI_MODULE=djangoblog.wsgi # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/server/python/djangoblog/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/server/python/djangoblog/venv/bin/gunicorn -b 0.0.0.0:8000  ${DJANGO_WSGI_MODULE}:application \
	--name $NAME \
	--workers $NUM_WORKERS \
	--user=$USER --group=$GROUP \
	--log-level=debug \
	--log-file=- &
