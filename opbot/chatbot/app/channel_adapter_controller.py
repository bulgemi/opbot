# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask_restplus import fields
from . import api

channel_adapter = api.model('ChannelAdapter', {"channel_id": fields.String,
                                               "event_uid": fields.String,
                                               "event_msg": fields.String})

