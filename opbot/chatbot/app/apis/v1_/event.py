# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask_restplus import Namespace, fields


class EventDto(object):
    api = Namespace('events', description='Channel Adapter REST APIs')
    event = api.model('event', {"channel_id": fields.String(required=True, description='Channel ID'),
                                "event_uid": fields.String(required=True, description='Event UID'),
                                "event_msg": fields.String(required=True, description='Event Message')})
