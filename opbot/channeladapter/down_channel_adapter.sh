#!/bin/sh

cd $OPBOT_HOME/channeladapter;
ps -ef |grep channeladapter_celery |grep -v grep |awk '{print $2}' |xargs kill -9;
