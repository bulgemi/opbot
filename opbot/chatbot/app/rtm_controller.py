# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
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
        create a new rtm
        :return:
        """
        current_app.logger.debug("payload(%r)=<%r>" % (type(rtm_a.payload),
                                                       rtm_a.payload))
        return rtm_a.payload, 201
