# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import asyncio
import websockets
from slacker import Slacker
sys.path.append(os.getenv('OPBOT_HOME'))
from chatbot.app.config import Config


async def execute_bot(end_point):
    ws = await websockets.connect(end_point)
    while True:
        message_json = await ws.recv()
        print(message_json)


if __name__ == '__main__':
    token = Config.SLACK_TOKEN
    slack = Slacker(token)
    response = slack.rtm.start()
    endpoint = response.body['url']

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(execute_bot(endpoint))
    asyncio.get_event_loop().run_forever()
