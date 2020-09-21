# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Slack으로부터 RTM을 이용하여 메시지를 받아온다.
수신된 메시지는 채널명과 text를 추출하여, Chatbot으로 REST API로 전송.
"""
import re
import json
import sys
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import websockets
from websockets.exceptions import ConnectionClosedError
import requests
from slacker import Slacker
import slack
from config import Config


class AsyncIoReceiver(object):
    """
    asyncio receiver object
    :return:
    """
    def __init__(self):
        logger = logging.getLogger('asyncio_receiver')

        # logging
        if os.path.isdir(Config.LOG_DIR) is False:
            os.mkdir(Config.LOG_DIR)

        log_full_path = "{}/{}".format(Config.LOG_DIR, Config.LOG_FILE_ASYNCIO_RECEIVER)
        file_handler = RotatingFileHandler(log_full_path,
                                           maxBytes=1024*100,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
        logger.setLevel(Config.LOG_LEVEL_ASYNCIO_RECEIVER)
        logger.addHandler(file_handler)

        self.logger = logger
        self.client = slack.WebClient(token=Config.SLACK_TOKEN)
        self.slack = Slacker(Config.SLACK_TOKEN)
        resp = self.slack.rtm.start()
        self.endpoint = resp.body['url']
        self.channels_list = None
        self.hello = False

    def set_hello(self):
        self.hello = True

    def set_channels_list(self):
        """
        채널 리스트를 추출/가공.
        :return:
        """
        channels_info = self.client.channels_list()

        if channels_info['ok'] is False:
            sys.exit()

        channels = channels_info['channels']

        channels_list = dict()

        for channel in channels:
            channels_list[channel['id']] = "#{}".format(channel['name'])
        self.channels_list = channels_list

        self.logger.debug("=====>(%r)<%r>" % (type(self.channels_list), self.channels_list))

    def call_rest_api(self, channel, text, user, ts):
        api_host = "http://127.0.0.1:9595/api/1/rtms/"
        data = {'channel': channel,
                'message': text,
                'user': user,
                'ts': ts}

        self.logger.debug("data=<%r>" % data)

        try:
            r = requests.post(api_host, json=data)
            return r
        except requests.exceptions.RequestException as e:
            self.logger.error("!%s!" % e)
            raise e


async def asyncio_recv(end_point, air):
    """
    비동기 응답 처리.
    :param end_point:
    :param air:
    :return:
    """
    ws = await websockets.connect(end_point)

    while True:
        try:
            message_str = await ws.recv()
        except ConnectionClosedError as e:
            air.logger.error("Error: (%d) %r" % (e.code, e.reason))
            from time import sleep
            sleep(3)
            ws = await websockets.connect(end_point)
            continue

        # todo: replace 해야 할 항목 확인 필요.
        json_acceptable_string = message_str.replace("'", "\'").replace('"', '\"').replace('\\\\"', '\\"')

        air.logger.debug("(%r)<%r>" % (type(json_acceptable_string), json_acceptable_string))

        message_json = json.loads(json_acceptable_string)

        if message_json['type'] == 'hello':
            air.set_hello()
        elif message_json['type'] == 'message' and 'client_msg_id' in message_json:
            air.logger.debug("(%r)<%r>" % (type(message_json), message_json))
            try:
                air.call_rest_api(air.channels_list[message_json['channel']],
                                  message_json['text'],
                                  message_json['user'],
                                  message_json['ts'])
            except requests.exceptions.RequestException as e:
                pass
        else:
            pass


if __name__ == '__main__':
    air = AsyncIoReceiver()
    air.set_channels_list()

    # loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(asyncio_recv(air.endpoint, air))
    asyncio.get_event_loop().run_forever()
