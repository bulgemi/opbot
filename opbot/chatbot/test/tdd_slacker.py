# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
from slacker import Slacker
import websocket
import json
sys.path.append(os.getenv('OPBOT_HOME'))
from chatbot.app.config import Config


class SlackerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        token = Config.SLACK_TOKEN
        self.slack = Slacker(token)

    def test_post_message(self):
        text = "test, 테스크, !@#$"
        channel = '#opbot_swing'
        username = 'opbot'
        attachments=None

        self.slack.chat.post_message(text=text,
                                     channel=channel,
                                     username=username,
                                     attachments=attachments)

    def test_post_message_attachments(self):
        text = None
        channel = '#opbot_swing'
        username = 'opbot'
        attachments = [{
            "color": "#36a64f",
            "title": "테스트",
            "title_link": "http://naver.com/",
            "fallback": "테스트 알림",
            "text": "파일 첨부 테스트."
        }]

        self.slack.chat.post_message(text=text,
                                     channel=channel,
                                     username=username,
                                     attachments=attachments)

    def test_rtm_recv(self):
        response = self.slack.rtm.start()
        sock_endpoint = response.body['url']
        print("<%s>" % sock_endpoint)
        slack_socket = websocket.create_connection(sock_endpoint)
        print("%r" % slack_socket.recv())

    def test_slack_web_client(self):
        import slack

        client = slack.WebClient(token=Config.SLACK_TOKEN)

        client.chat_postMessage(
            channel="#opbot_swing",
            username='opbot',
            text="Hello from your app! :tada:"
        )

    def test_formatting_with_block_kit(self):
        import slack

        client = slack.WebClient(token=Config.SLACK_TOKEN)

        rc = client.chat_postMessage(
            channel="#opbot_swing",
            username='opbot',
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Danny Torrence left the following review for your property:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room " +
                                "237 was far too rowdy, whole place felt stuck in the 1920s."
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://images.pexels.com/photos/750319/pexels-photo-750319.jpeg",
                        "alt_text": "Haunted hotel image"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Average Rating*\n1.0"
                        }
                    ]
                }
            ]
        )

        print(rc)

    def test_formatting_with_block_kit_button(self):
        text = None
        channel = '#opbot_swing'
        username = 'opbot'
        attachments = [{
            "title": "TP Timeout 발생.",
            "text": "아래와 같은 원인 분석을 진행할 수 있습니다.",
            "callback_id": "task_run",
            "color": "#3AA3E3",
            "actions": [
                {
                    "name": "system_status",
                    "text": "시스템 상태 분석",
                    "type": "button",
                    "value": "system_status",
                    "action_id": "button",
                },
                {
                    "name": "tp_status",
                    "text": "TP 상태 분석",
                    "type": "button",
                    "value": "tp_status",
                    "action_id": "tp_status",
                    "style": "primary"
                },
                {
                    "name": "db_status",
                    "text": "DB 상태 분석",
                    "type": "button",
                    "value": "db_status",
                    "action_id": "db_status",
                    "style": "danger"
                },
                {
                    "name": "channel_status",
                    "text": "EAI/MCG 상태 분석",
                    "type": "button",
                    "value": "channel_status",
                    "action_id": "channel_status"
                },
            ]
        }]

        response = self.slack.chat.post_message(text=text,
                                                channel=channel,
                                                username=username,
                                                attachments=attachments)
        print(response.body)

    def test_listing_channels(self):
        import slack

        client = slack.WebClient(token=Config.SLACK_TOKEN)

        rc = client.channels_list()
        print(rc)

        rc = client.channels_list(exclude_archived=1)
        print(rc)

    def test_getting_channel_info(self):
        import slack

        client = slack.WebClient(token=Config.SLACK_TOKEN)
        rc = client.channels_info(channel="#opbot_swing")
        print(rc)

    def test_users_list(self):
        import slack

        client = slack.WebClient(token=Config.SLACK_TOKEN)
        rc = client.users_list()
        print(rc)

        for member in rc['members']:
            print(member['id'], member['name'], member['real_name'])

    def test_uploading_files(self):
        import slack

        client = slack.WebClient(token=Config.SLACK_TOKEN)
        client.files_upload(
            channels="#opbot_swing",
            username='opbot',
            file="top.pdf",
            title="시스템_상태_분석 보고서"
        )
