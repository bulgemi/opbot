# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Chatbot REST API Server
"""
import sys
import os
import re
import slack
from flask import current_app
from sqlalchemy import and_
from slacker import Slacker
from redis import Redis
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import ChannelInfo, EventHistory, TaskInfo
from chatbot.app.config import Config
from collector.app.collect import Collector


class ChatBot(object):
    def __init__(self, db):
        token = Config.SLACK_TOKEN

        self.__slack = Slacker(token)
        self.__client = slack.WebClient(token=Config.SLACK_TOKEN)
        self.__db = db
        self.__r = Redis(host='localhost', port=6389, db=0)
        self.__c = Collector(db)
        self.__recommend_uri = Config.RECOMMENDER_URI

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

    def set_current_subjects(self, out_channel_id, event_uid):
        """
        현재 처리 중인 event subject 세팅.
        :param out_channel_id:
        :param event_uid:
        :return:
        """
        hash_key = "opbot_subjects"
        data = {out_channel_id: event_uid}
        return self.__r.hmset(hash_key, data)

    def get_current_subjects(self, out_channel_id):
        """
        현재 처리 중인 event subject 반환.
        :param out_channel_id:
        :return:
        """
        hash_key = "opbot_subjects"
        result = self.__r.hmget(hash_key, out_channel_id)

        if result[0] is None or len(result) <= 0:
            return None
        else:
            return result[0].decode('utf-8')

    def del_current_subjects(self, out_channel_id):
        """
        현재 처리 중인 event subject 삭제.
        :param out_channel_id:
        :return:
        """
        hash_key = "opbot_subjects"
        self.__r.hdel(hash_key, out_channel_id)

    def get_context(self, out_channel_id, event_uid):
        """
        chat context 반환
        :param out_channel_id:
        :param event_uid:
        :return:
        """
        hash_key = "opbot_events{}".format(out_channel_id)
        context = self.__r.hget(hash_key, event_uid)

        # default context 는 분석, 'A': 분석, 'S': 조치
        if context is None:
            data = {event_uid: 'A'}
            self.__r.hmset(hash_key, data)
            context = self.__r.hget(hash_key, event_uid)

        return context.decode('utf-8')

    def get_context_one(self, out_channel_id):
        """
        chat contexts 중 하나 반환.
        :param out_channel_id:
        :return:
        """
        hash_key = "opbot_events{}".format(out_channel_id)
        contexts = self.__r.hgetall(hash_key)

        for key, value in contexts.items():
            return key.decode('utf-8'), value.decode('utf-8')
        return None, None

    def del_context(self, out_channel_id, event_uid):
        """
        chat context 삭제
        :param out_channel_id:
        :param event_uid:
        :return:
        """
        hash_key = "opbot_events{}".format(out_channel_id)
        self.__r.hdel(hash_key, event_uid)

    def set_context_a(self, out_channel_id, event_uid):
        """
        chat context: 분석 모드
        default context 는 분석, 'A': 분석, 'S': 조치
        :param out_channel_id:
        :param event_uid:
        :return:
        """
        # default context 는 분석, 'A': 분석, 'S': 조치
        hash_key = "opbot_events{}".format(out_channel_id)
        data = {event_uid: 'A'}
        return self.__r.hmset(hash_key, data)

    def set_context_s(self, out_channel_id, event_uid):
        """
        chat context: 조치 모드
        default context 는 분석, 'A': 분석, 'S': 조치
        :param out_channel_id:
        :param event_uid:
        :return:
        """
        # default context 는 분석, 'A': 분석, 'S': 조치
        hash_key = "opbot_events{}".format(out_channel_id)
        data = {event_uid: 'S'}
        return self.__r.hmset(hash_key, data)

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
        opinions = "과거 이력을 기반으로 분석한 작업 유효확률는 아래와 같습니다.\n\n"

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

        analysis_opinion = self.analysis_opinion(channel)

        if analysis_opinion is not None:
            attachments.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":information_source: *{}*".format(analysis_opinion)
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

    def put_end(self, channel, message=None):
        """
        out channel(slack) 작업 채널에 종료 메시지 전송.
        :param channel:
        :param message:
        :return:
        """
        attachments = list()

        if message is not None:
            attachments.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}*".format(message),
                }
            })

        desc = ""
        cause = self.get_cause(channel)
        solution = self.get_solution(channel)

        if cause is not None:
            desc += "> 원인: {}".format(cause)

        if solution is not None:
            desc += "\n> 조치: {}".format(solution)

        attachments.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": desc
            }
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

    def put_collect(self, event_uid, task_id, exec_type):
        """
        작업자가 수행한 이력을 Collector 에 전송.
        작업 요청은 Celery 기반의 Async task queue 사용.
        :param event_uid:
        :param task_id:
        :param exec_type:
        :return:
        """
        return self.__c.action_info_get(event_uid, task_id, exec_type)

    def get_cause(self, out_channel_id):
        """
        이벤트 원인 내용 반환.
        Recommender 에 요청, REST API 사용
        :param out_channel_id:
        :return:
        """
        # Todo: 이벤트의 원인을 추론, M/L
        return "'DB Session Lock'으로 인한 거래 Timeout 발생"

    def get_solution(self, out_channel_id):
        """
        이벤트 조치 내용 반환.
        Recommender 에 요청, REST API 사용
        :param out_channel_id:
        :return:
        """
        # Todo: 이벤트의 해결을 추론, M/L
        return "'DB_Session_Lock_제거' 수행"

    def task_recommend(self, out_channel_id):
        """
        분석/조치 task 추천 정보 Recommender 에 요청.
        요청은 REST API 사용
        :param out_channel_id: OUT 채널 ID
        :return:
        """
        import requests

        context_key = self.get_current_subjects(out_channel_id)
        msg = self.get_event_message(context_key)

        data = {'event_msg': msg,
                'action_type': self.get_context(out_channel_id, context_key)}
        task_list = list()

        try:
            r = requests.post(self.__recommend_uri, json=data)

            if r.status_code == 201:
                for task in r.json():
                    task_list.append(task['task_id'])
            else:
                current_app.logger.error("return error(%d)" % r.status_code)
                return None
        except requests.exceptions.RequestException as e:
            current_app.logger.error("!%s!" % e)
            return None
        return task_list

    def task_opinion(self, out_channel_id):
        """
        발생한 event 유형을 분석하고 이에 적합한 분석/조치 task 적합도 제공
        REST API 를 이용하여 Recommander 로부터 의견 수신
        :param out_channel_id: OUT 채널 ID
        :return:
        """
        import requests

        context_key = self.get_current_subjects(out_channel_id)
        msg = self.get_event_message(context_key)

        data = {'event_msg': msg,
                'action_type': self.get_context(out_channel_id, context_key)}
        opinion_list = list()

        try:
            r = requests.post(self.__recommend_uri, json=data)

            if r.status_code == 201:
                for task in r.json():
                    opinion_list.append("{}: {} %".format(task['task_id'], task['percentage']))
            else:
                current_app.logger.error("return error(%d)" % r.status_code)
                return None
        except requests.exceptions.RequestException as e:
            current_app.logger.error("!%s!" % e)
            return None
        return opinion_list

    def analysis_opinion(self, out_channel_id):
        """
        발생한 event 유형을 분석하고 이에 적합한 분석/조치 의견 제공
        REST API 를 이용하여 Recommander 로부터 의견 수신
        :param out_channel_id: OUT 채널 ID
        :return:
        """
        import requests

        context_key = self.get_current_subjects(out_channel_id)
        msg = self.get_event_message(context_key)

        data_a = {'event_msg': msg, 'action_type': 'A'}
        data_s = {'event_msg': msg, 'action_type': 'S'}
        opinion = ""

        try:
            cause = "None"
            work = "None"
            r_a = requests.post(self.__recommend_uri, json=data_a)

            if r_a.status_code != 201:
                current_app.logger.error("return error r_a(%d)" % r_a.status_code)
                return None

            r_s = requests.post(self.__recommend_uri, json=data_s)

            if r_s.status_code != 201:
                current_app.logger.error("return error r_s(%d)" % r_s.status_code)
                return None

            if len(r_s.json()) > 0:
                cause_info = r_s.json()[0]
                cause = self.__get_task_cause(cause_info['task_id'])

            if self.get_context(out_channel_id, context_key) == 'A':
                if len(r_a.json()) > 0:
                    work_info = r_a.json()[0]
                    work = work_info['task_id']
                opinion = "장애원인은 '{}'일 확률이 높으며, 분석작업은 '{}'을(를) 추천합니다.".format(cause, work)
            else:
                if len(r_s.json()) > 0:
                    work_info = r_s.json()[0]
                    work = work_info['task_id']
                opinion = "장애원인은 '{}'일 확률이 높으며, 조치작업은 '{}'을(를) 추천합니다.".format(cause, work)
        except requests.exceptions.RequestException as e:
            current_app.logger.error("!%s!" % e)
            return ""
        return opinion

    def get_event_message(self, event_uid):
        """
        event_uid 에 해당하는 event message 반환.
        :param event_uid:
        :return:
        """
        current_app.logger.debug("event_uid=<%r>" % event_uid)

        stmt = self.__db.session.query(EventHistory)
        stmt = stmt.with_entities(EventHistory.event_msg)
        event_message = stmt.filter(EventHistory.event_uid == event_uid.strip()).first()
        return event_message[0]

    def __get_task_cause(self, task_id):
        """
        발생 원인 반환.
        :param task_id:
        :return:
        """
        stmt = self.__db.session.query(TaskInfo)
        stmt = stmt.with_entities(TaskInfo.cause)
        cause = stmt.filter(TaskInfo.task_id == task_id.strip()).first()
        return cause[0]

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

    def say_hello(self, msg):
        """
        인사 처리.
        todo: 임시처리
        :param msg:
        :return: hello list
        """
        # p = re.compile(r"([#])([ㄱ-ㅎ가-핳a-zA-Z0-9]+)([#])")
        p = re.compile(r"안녕|안뇽|헬로|하이|방가|\bhi\b|\bhello\b|할룽|오피봇|\bopbot\b")

        if len(msg) <= 0:
            return []

        mc = p.findall(msg)
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
                if len(task_list) < int(tmp):
                    return None
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
            title=title)
