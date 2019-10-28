# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
from flask import current_app
from flask_restplus import Resource
from .apis.v1_.event import EventDto
sys.path.append(os.getenv('OPBOT_HOME'))

event_a = EventDto.api
event_m = EventDto.event


@event_a.route('/')
class AsyncEvent(Resource):
    @event_a.doc('create a New Channel Adapter Event')
    @event_a.expect(event_m)
    @event_a.marshal_with(event_m, code=201)
    def post(self):
        """
        create a new channel adapter event
        1.이벤트 수신
        2.channel 정보 조회
        3.분석/조치 task 추천 정보 조회
        4.등록된 채널에 메시지 전송
        :return:
        """
        # 1.이벤트 수신
        current_app.logger.debug("payload(%r)=<%r>" % (type(event_a.payload),
                                                       event_a.payload))
        current_app.logger.debug("bot=<%r>" % current_app.bot)

        event_info = event_a.payload
        # 2.channel 정보 조회
        out_channels = current_app.bot.channel_read(event_info['channel_id'])

        # 3.등록된 채널에 메시지 전송
        if len(out_channels) > 0:
            for channel_info in out_channels:
                current_app.logger.debug("channel_info=<%r, %r, %r>"
                                         % (channel_info[0], channel_info[1], channel_info[2]))

                if channel_info[0] == 'B':
                    current_app.bot.put_broadcast(channel=channel_info[1], message=event_info['event_msg'])
                elif channel_info[0] == 'C':
                    # context 분석'A'로 설정.
                    current_app.bot.set_context_a(channel_info[1])
                    # 분석 task 추천 정보 조회
                    anal_tasks = current_app.bot.task_recommend(event_info['channel_id'], channel_info[1])
                    current_app.bot.put_chat(channel=channel_info[1], message=event_info['event_msg'], tasks=anal_tasks)
                else:
                    current_app.logger.error("invalid channel type!")
                    pass

        return event_a.payload, 201
