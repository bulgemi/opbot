#!/bin/sh
cd $OPBOT_HOME/chatbot;
ps -ef |grep python |grep asyncio_receiver |grep -v grep |awk '{print $2}' |xargs kill -9;
ps -ef |grep chatbot_celery |grep -v grep |awk '{print $2}' |xargs kill -9;
ps -ef |grep manage:app | grep 9595 |grep -v grep |awk '{print $2}' |xargs kill -9;
