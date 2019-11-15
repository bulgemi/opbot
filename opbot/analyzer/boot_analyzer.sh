#!/bin/sh

cd $OPBOT_HOME/analyzer;
celery -A manage.celery beat  --loglevel=DEBUG -f /home/donghun/PycharmProjects/opbot/logs/analyzer_celerybeat.log &
celery -A manage.celery worker -c 2 --loglevel=DEBUG -f /home/donghun/PycharmProjects/opbot/logs/analyzer_celery.log &
