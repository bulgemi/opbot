#!/bin/sh
cd $OPBOT_HOME/recommender;
ps -ef |grep manage:app |grep 5959 |grep -v grep |awk '{print $2}' |xargs kill -9;
