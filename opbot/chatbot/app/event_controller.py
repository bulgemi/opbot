# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
from flask_restplus import Resource
from .apis.v1_.event import EventDto

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
        :return:
        """
        current_app.logger.debug("payload(%r)=<%r>" % (type(event_a.payload),
                                                       event_a.payload))
        return event_a.payload, 201
