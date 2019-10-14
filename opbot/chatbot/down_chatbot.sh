#!/bin/sh
cd $OPBOT_HOME/chatbot;
ps -ef |grep python |grep asyncio_receiver |grep -v grep |awk '{print $2}' |xargs kill -9;
