# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask_restplus import Namespace, fields


class EventDto(object):
    api = Namespace('events', description='Recommender REST APIs')
    event = api.model('event', {"action_type": fields.String(required=True, description="'A' or 'S'"),
                                "event_msg": fields.String(required=True, description='Event Message')})
