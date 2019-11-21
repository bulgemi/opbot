# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
from flask import current_app
from flask_restplus import Resource, fields, marshal_with
from .apis.v1_.event import EventDto
sys.path.append(os.getenv('OPBOT_HOME'))

event_a = EventDto.api
event_m = EventDto.event
mfields = {'task_id': fields.Raw, 'percentage': fields.Raw}


@event_a.route('/')
class AsyncEvent(Resource):
    @event_a.doc('create a New Recommend Event')
    @event_a.expect(event_m)
    @event_a.marshal_with(mfields, code=201)
    def post(self):
        """
        create a new Recommend event
        1.이벤트 수신
        2.사용가능한 TASK 조회
        3.TASK 추천도(백분율) 계산
        4.추천도 기준으로 정렬된 TASK LIST 반환
        :return:
        """
        # 1.이벤트 수신
        current_app.logger.debug("payload(%r)=<%r>" % (type(event_a.payload),
                                                       event_a.payload))

        event_info = event_a.payload
        recommender = current_app.recommender
        res = recommender.recommend_info_get(event_info['event_msg'], event_info['action_type'])
        current_app.logger.debug("res=<%r>" % res)

        return res, 201
