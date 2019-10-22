# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from random import randrange
from flask import current_app
from flask_restplus import Resource
from .apis.v1_.rtm import RtmDto

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

        task_list = current_app.bot.parse_command(rtm_msg['message'])

        recommend_tasks = None

        if len(task_list) <= 0:
            err_messages = [
                "죄송해요. 다시 입력해주세요.",
                "죄송해요. 알수 없는 명령입니다.",
                "뭔 말이여?",
                "Sorry, Please try again.",
                "죄송해요. 이해를 못 했습니다."
            ]
            current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                          message=err_messages[randrange(len(err_messages))])
        else:
            in_channel_id = current_app.bot.get_in_channel_info(rtm_msg['channel'], 'C')
            recommend_tasks = current_app.bot.task_recommend(in_channel_id)

            # current_app.logger.debug("recommend_tasks=<%r>" % recommend_tasks)

        for task in task_list:
            task_id = current_app.bot.get_task_id(recommend_tasks, task)

            result = manage.task_execute.delay(task_id)
            result.wait()
            # current_app.bot.put_broadcast(channel=rtm_msg['channel'],
            #                               message="[{}] 수행하였습니다.".format(task_id))

        return res_msg, 201
