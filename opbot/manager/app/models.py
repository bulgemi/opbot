# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from . import db


class EventHistory(db.Model):
    event_uid = db.Column(db.String(256), primary_key=True)
    event_msg = db.Column(db.Text)
    channel_id = db.Column(db.String(256))
    create_date = db.Column(db.String(16))

    def __repr__(self):
        return '<event_uid %r, channel_id %r>' % (self.event_uid, self.channel_id)


class ChannelInfo(db.Model):
    in_channel_id = db.Column(db.String(256), primary_key=True)
    out_channel_type = db.Column(db.String(1), primary_key=True)
    out_channel_id = db.Column(db.String(256), primary_key=True)
    out_channel_name = db.Column(db.String(512))

    def __repr__(self):
        return '<in_channel_id %r, out_channel_type %r, out_channel_id %r>'\
               % (self.in_channel_id, self.out_channel_type, self.out_channel_id)
