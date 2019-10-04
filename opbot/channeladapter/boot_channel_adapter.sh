#!/bin/sh

cd $OPBOT_HOME/channeladapter;
celery -A manage.celery beat  --loglevel=DEBUG -f channeladapter_celerybeat.log &
celery -A manage.celery worker -c 2 --loglevel=DEBUG -f channeladapter_celery.log &
