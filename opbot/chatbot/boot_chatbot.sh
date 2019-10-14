#!/bin/sh
cd $OPBOT_HOME/chatbot;
python app/asyncio_receiver.py &
