#!/bin/sh
cd $OPBOT_HOME/chatbot;
python app/asyncio_receiver.py &
celery -A manage.celery worker -c 2 --loglevel=DEBUG -f /home/donghun/PycharmProjects/opbot/logs/chatbot_celery.log &
gunicorn -w 4 -b 0.0.0.0:9595 manage:app &
