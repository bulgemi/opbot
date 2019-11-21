#!/bin/sh
cd $OPBOT_HOME/recommender;
gunicorn -w 4 -b 0.0.0.0:5959 manage:app &
