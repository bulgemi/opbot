# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask_restplus import Namespace, fields


class RtmDto(object):
    api = Namespace('rtms', description='Slack RTM REST APIs')
    rtm = api.model('rtm', {"channel": fields.String(required=True, description='Slack Channel'),
                            "message": fields.String(required=True, description='Slack Chat Message'),
                            "user": fields.String(required=True, description='Slack Chat User'),
                            "ts": fields.String(required=True, description='Slack TS')})
