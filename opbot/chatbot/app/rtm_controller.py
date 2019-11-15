# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from random import randrange
from flask import current_app
from flask_restplus import Resource
from .apis.v1_.rtm import RtmDto
from redis.exceptions import DataError

rtm_a = RtmDto.api
rtm_m = RtmDto.rtm


@rtm_a.route('/')
class AsyncRtm(Resource):
    @rtm_a.doc('create a New Slack RTM')
    @rtm_a.expect(rtm_m)
    @rtm_a.marshal_with(rtm_m, code=201)
    def post(self):
        """
        RTM 수신.
        1.rtm 수신
        2.message 구문 분석
        3.if 구문내 수행 명령 존재 시, async task 요청
        :return:
        """
        import os
        import sys
        sys.path.append(os.getenv('OPBOT_HOME')+"/chatbot")
        import manage

        res_msg = {
            "channel": "opbot",
            "ok": True,
            "message": "success"
        }

        current_app.logger.debug("payload(%r)=<%r>" % (type(rtm_a.payload),
                                                       rtm_a.payload))

        rtm_msg = rtm_a.payload

        command_list = current_app.bot.parse_command(rtm_msg['message'])

        recommend_tasks = None

        if len(command_list) <= 0:
            hello_messages = [
                "네, 안녕하세요.",
                "Hi.",
                "안녕하세요."
            ]
            err_messages = [
                "죄송해요. 다시 입력해주세요.",
                "죄송해요. 알수 없는 명령입니다.",
                "뭔 말이여?",
                "Sorry, Please try again.",
                "죄송해요. 이해를 못 했습니다."
            ]
            hello = current_app.bot.say_hello(rtm_msg['message'])

            if len(hello) <= 0:
                current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                              message=err_messages[randrange(len(err_messages))])
            else:
                current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                              message=hello_messages[randrange(len(hello_messages))])
        else:
            in_channel_id = current_app.bot.get_in_channel_info(rtm_msg['channel'], 'C')

        for task in command_list:
            current_app.logger.debug("task=<%r>" % task)

            if task == '!조치!':
                # context 상태 변경.
                # todo: code refactoring 필요.
                try:
                    current_app.bot.set_context_s(rtm_msg['channel'],
                                                  current_app.bot.get_current_subjects(rtm_msg['channel']))
                except DataError:
                    msg = "처리할 이벤트가 없습니다."
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=msg)
                    return res_msg, 201
                # 조치 Task
                # 3.분석 task 추천 정보 조회
                anal_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                current_app.bot.put_chat(channel=rtm_msg['channel'], message=None, tasks=anal_tasks)
            elif task == '!분석!':
                # context 상태 변경.
                # todo: code refactoring 필요.
                try:
                    current_app.bot.set_context_a(rtm_msg['channel'],
                                                  current_app.bot.get_current_subjects(rtm_msg['channel']))
                except DataError:
                    msg = "처리할 이벤트가 없습니다."
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=msg)
                    return res_msg, 201
                anal_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                current_app.bot.put_chat(channel=rtm_msg['channel'], message=None, tasks=anal_tasks)
            elif task == '!종료!':
                # context 상태 변경.
                # context 삭제.
                # todo: code refactoring 필요.
                try:
                    current_app.bot.del_context(rtm_msg['channel'],
                                                current_app.bot.get_current_subjects(rtm_msg['channel']))
                except DataError:
                    msg = "처리할 이벤트가 없습니다."
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                                  message=msg)
                    return res_msg, 201

                # 잔여 context 가 있는지 확인
                event_uid, _ = current_app.bot.get_context_one(rtm_msg['channel'])

                current_app.logger.debug("event_uid=<%r>" % event_uid)

                if event_uid is None:
                    # subject 삭제.
                    current_app.bot.del_current_subjects(rtm_msg['channel'])
                    # 종료 처리
                    msg = "상황 종료되었습니다. 감사합니다."
                    # 전체 채널에 공지
                    out_channels = current_app.bot.channel_read(in_channel_id)

                    if len(out_channels) > 0:
                        for channel_info in out_channels:
                            if channel_info[0] == 'B':
                                current_app.bot.put_end(channel=channel_info[1], message=msg)
                            elif channel_info[0] == 'C':
                                current_app.bot.put_end(channel=channel_info[1], message=msg)
                            else:
                                pass
                    break
                else:
                    # 다음 event 처리
                    current_app.bot.set_context_a(rtm_msg['channel'], event_uid)
                    current_app.bot.set_current_subjects(rtm_msg['channel'], event_uid)

                    # 분석 task 추천 정보 조회
                    message = current_app.bot.get_event_message(event_uid)
                    anal_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                    current_app.bot.put_chat(channel=rtm_msg['channel'], message=message, tasks=anal_tasks)
            else:
                recommend_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                # current_app.logger.debug("recommend_tasks=<%r>" % recommend_tasks)
                task_id = current_app.bot.get_task_id(recommend_tasks, task)

                if task_id is None:
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                                  message="죄송해요. 알수 없는 명령입니다.")
                else:
                    # Task 수행 비동기 처리.
                    result = manage.task_execute.delay(task_id, rtm_msg['channel'])
                    result.wait()
                    # put collector, 비동기 처리.
                    ctx = current_app.bot.get_context(rtm_msg['channel'],
                                                      current_app.bot.get_current_subjects(rtm_msg['channel']))
                    c = manage.put_collector.delay(current_app.bot.get_current_subjects(rtm_msg['channel']),
                                                   task_id,
                                                   ctx)
                    c.wait()

        return res_msg, 201
