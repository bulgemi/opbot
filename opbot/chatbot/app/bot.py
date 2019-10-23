# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Chatbot REST Server
"""
import sys
import os
import re
import slack
from flask import current_app
from sqlalchemy import and_
from slacker import Slacker
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import ChannelInfo
from chatbot.app.config import Config


class ChatBot(object):
    def __init__(self, db):
        token = Config.SLACK_TOKEN

        self.__slack = Slacker(token)
        self.__client = slack.WebClient(token=Config.SLACK_TOKEN)
        self.__db = db
        self.__context = 'A'  # default context는 분석, 'A': 분석, 'S': 조치

    def __put_out_channel(self, channel, username='opbot', text=None, attachments=None):
        """
        out channel(slack) 이벤트 전송.
        :param channel:
        :param username:
        :param text:
        :param attachments:
        :return:
        """
        blocks = attachments
        return self.__client.chat_postMessage(channel=channel, username=username, blocks=blocks)

    def set_context_a(self):
        """
        분석 모드
        :return:
        """
        self.__context = 'A'

    def set_context_s(self):
        """
        조치 모드
        :return:
        """
        self.__context = 'S'

    def put_broadcast(self, channel, message=None):
        """
        out channel(slack) 공유 채널에 이벤트를 브로드케스팅.
        공유 채널: 이해관계자가 모두 포함되어 있는 단체 채팅방
        :param channel:
        :param message:
        :return:
        """
        attachments = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}*".format(message),
                }
            },
        ]
        return self.__put_out_channel(channel=channel, attachments=attachments)

    def put_chat(self, channel, message=None, tasks=None):
        """
        out channel(slack) 작업 채널에 이벤트를 전송.
        착업 채널: 이벤트 처리 작업자가 사용하는 패쇄 채팅방
        :param channel:
        :param message:
        :param tasks:
        :return:
        """
        task_list = list()
        opinions = "과거 이력을 기반으로 분석한 적합도 수치는 아래와 같습니다.\n\n"

        for index, task in enumerate(tasks):
            tmp = {
                "type": "mrkdwn",
                "text": "{}.{}".format(index+1, task),
            }
            task_list.append(tmp)

        # 발생한 event 유형을 분석하고 이에 적합한 분석/조치 task에 대한 의견 제공
        for opinion in self.task_opinion(channel):
            opinions += "*{}*\n".format(opinion)

        attachments = list()

        if message is not None:
            attachments.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}*".format(message),
                }
            })
        attachments.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": opinions
                    }
                ]
            })
        attachments.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "> 아래와 같은 분석 작업을 수행할 수 있습니다.\n"
                            "> 수행방법: `!번호!`, `!작업명!`, `!번호.작업명!`",
                }
            })
        attachments.append({
                "type": "divider"
            })
        attachments.append({
                "type": "section",
                "fields": task_list
            })
        return self.__put_out_channel(channel=channel, attachments=attachments)

    def choose_as(self, channel):
        """
        수행모드 선택 메시지 전송.
        :param channel:
        :return:
        """
        attachments = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "> 계속 분석을 진행하려면 `!분석!`, 조치를 진행하려면 `!조치!`를 입력하세요.\n"
                            "> 상황을 종료하려면 `!종료!`를 입력하세요.",
                }
            },
        ]
        return self.__put_out_channel(channel=channel, attachments=attachments)

    def choose_complete(self, channel):
        """
        수행모드 선택 메시지 전송.
        :param channel:
        :return:
        """
        attachments = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "조치 작업을 종료하시겠습니까?`\n"
                            "> 종료하려면 `!종료!`를 입력하세요.",
                }
            },
        ]
        return self.__put_out_channel(channel=channel, attachments=attachments)

    def interactive_chat(self):
        """
        out channel(slack)과 web hook 방식으로 interactive message 처리.
        :return:
        """
        pass

    def task_execute(self, task_id, out_channel_id):
        """
        작업자가 요청한 task를 TaskExecutor 에 전송.
        작업 요청은 Celery 기반의 Async task queue 사용.
        :param task_id:
        :param out_channel_id:
        :return:
        """
        from .task_executor import TaskExecutor

        current_app.logger.debug("task_id=<%r>, out_channel_id=<%r>" % (task_id, out_channel_id))

        task_executor = TaskExecutor(task_id, out_channel_id, self.__db)
        task_executor.run_task()

        return True

    def log_collect(self):
        """
        작업자가 수행한 이력을 Collector 에 전송.
        작업 요청은 Celery 기반의 Async task queue 사용.
        :return:
        """
        pass

    def task_recommend(self, channel_id):
        """
        분석/조치 task 추천 정보 Recommender 에 요청.
        요청은 REST API 사용
        :param channel_id: 이벤트 발생 채널 ID
        :return:
        """
        # Todo: recommender 연동, task 명 공백 없음.
        if self.__context == 'A':
            tasks = ["DB_상태_분석", "EAI/MCG_상태_분석", "시스템_상태_분석", "TP_상태_분석"]
        else:
            tasks = ["DB_Session_Lock_제거", "EAI_Queue_Purge", "TP_재기동"]
        return tasks

    def task_opinion(self, channel_id):
        """
        발생한 event 유형을 분석하고 이에 적합한 분석/조치 task에 대한 의견 제공
        REST API를 이용하여 Recommander로부터 의견 수신
        :param channel_id: 이벤트 발생 채널 ID
        :return:
        """
        # Todo: recommender 연동, task 명 공백 없음.
        if self.__context == 'A':
            opinion = ["DB_상태_분석: 85.3 %", "EAI/MCG_상태_분석: 13.2 %", "TP_상태_분석: 1.5 %", "시스템_상태_분석: 0%"]
        else:
            opinion = ["DB_Session_Lock_제거: 95 %", "EAI_Queue_Purge: 15 %", "TP_재기동: 0 %"]

        return opinion

    def channel_read(self, in_channel_id):
        """
        channel_info 정보 조회.
        :param in_channel_id:
        :return:
        """
        stmt = self.__db.session.query(ChannelInfo)
        stmt = stmt.with_entities(ChannelInfo.out_channel_type,
                                  ChannelInfo.out_channel_id,
                                  ChannelInfo.out_channel_name)
        out_channel_info = stmt.filter(ChannelInfo.in_channel_id == in_channel_id.strip()).all()

        return out_channel_info

    def get_in_channel_info(self, out_channel_id, out_channel_type):
        """
        in_channel ID 조회
        :param out_channel_id:
        :param out_channel_type:
        :return:
        """
        stmt = self.__db.session.query(ChannelInfo)
        stmt = stmt.with_entities(ChannelInfo.in_channel_id)
        in_channel_info = stmt.filter(and_(ChannelInfo.out_channel_id == out_channel_id.strip(),
                                           ChannelInfo.out_channel_type == out_channel_type.strip())).first()

        return in_channel_info.in_channel_id

    def history_read(self):
        pass

    def parse_command(self, msg):
        """
        메시지 분석.
        0.공백 제거
        1.!번호! or !작업명! or !번호.작업명! 추출
        2.결과 반환.
        :param msg:
        :return: task list
        """
        # p = re.compile(r"([#])([ㄱ-ㅎ가-핳a-zA-Z0-9]+)([#])")
        p = re.compile(r"([!][ㄱ-ㅎ가-핳a-zA-Z0-9._/]+[!])")

        if len(msg) <= 0:
            return []

        mc = p.findall(msg.replace(" ", ""))
        return mc

    def get_task_id(self, task_list, command_message):
        """
        chatbot을 통해 수신된 명령어
        1.'!' 제거
        2.'.' split
        3.task 반환
        :param task_list:
        :param command_message:
        :return:
        """
        command = command_message.replace('!', '')
        command_split = command.split('.')

        if len(command_split) == 1:
            tmp = command_split[0].strip()

            if tmp.isdigit() is True:
                return task_list[int(tmp)-1]
            else:
                for task in task_list:
                    # current_app.logger.debug("====>%s, %s" % (task, tmp))

                    if task == tmp:
                        return task
        elif len(command_split) == 2:
            tmp1 = command_split[0].strip()
            tmp2 = command_split[1].strip()

            if tmp1.isdigit() is True:
                return task_list[int(tmp1)-1]
            else:
                for task in task_list:
                    current_app.logger.debug("%s, %s" % (task, tmp2))

                    if task == tmp2:
                        return task
        else:
            pass

        return None

    def upload_report(self, channels, file, title, username='opbot'):
        """
        보고서 업로드
        :param channels:
        :param file:
        :param title:
        :param username:
        :return:
        """
        return self.__client.files_upload(
            channels=channels,
            username=username,
            file=file,
            title=title
        )
