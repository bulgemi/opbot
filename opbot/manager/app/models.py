# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from . import db


class EventHistory(db.Model):
    event_uid = db.Column(db.String(256), primary_key=True)
    event_msg = db.Column(db.Text, nullable=False)
    channel_id = db.Column(db.String(256), nullable=False)
    create_date = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<event_uid %r, channel_id %r>' % (self.event_uid, self.channel_id)


class ChannelInfo(db.Model):
    in_channel_id = db.Column(db.String(256), primary_key=True)
    out_channel_type = db.Column(db.String(1), primary_key=True)
    out_channel_id = db.Column(db.String(256), primary_key=True)
    out_channel_name = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return '<in_channel_id %r, out_channel_type %r, out_channel_id %r>'\
               % (self.in_channel_id, self.out_channel_type, self.out_channel_id)


class TargetList(db.Model):
    task_id = db.Column(db.String(256), primary_key=True)
    host = db.Column(db.String(126), primary_key=True)
    port = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(126), nullable=False)
    passwd = db.Column(db.String(512), nullable=False)
    out_channel_id = db.Column(db.String(256), primary_key=True)
    adapter_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<task_id %r, host %r, out_channel_id %r>' \
               % (self.task_id, self.host, self.out_channel_id)


class TaskInfo(db.Model):
    task_id = db.Column(db.String(256), primary_key=True)
    task_type = db.Column(db.String(1), nullable=False)
    script_seq = db.Column(db.Integer, primary_key=True)
    script = db.Column(db.Text)

    def __repr__(self):
        return '<task_id %r, script_seq %r>' \
               % (self.task_id, self.script_seq)


class WorkHistory(db.Model):
    event_uid = db.Column(db.String(256), primary_key=True)
    outbound_task_id = db.Column(db.String(256), primary_key=True)
    exec_type = db.Column(db.String(1), nullable=True)
    create_date = db.Column(db.String(16), primary_key=True)

    def __repr__(self):
        return '<event_uid %r, outbound_task_id %r>' % (self.event_uid, self.outbound_task_id)


class RecommendBaseInfo(db.Model):
    pattern_id = db.Column(db.String(126), primary_key=True)
    message_pattern = db.Column(db.Text, nullable=False)
    outbound_task_id = db.Column(db.String(256), nullable=False)
    call_cnt = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<pattern_id %r, outbound_task_id %r, call_cnt %d>'\
               % (self.pattern_id, self.outbound_task_id, self.call_cnt)
