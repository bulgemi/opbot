#!/bin/sh

cd $OPBOT_HOME/analyzer;
ps -ef |grep analyzer_celery |grep -v grep |awk '{print $2}' |xargs kill -9;
