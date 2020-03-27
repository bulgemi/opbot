# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from . import db


class EventHistory(db.Model):
    """
    inbound 채널(swing)에서 발생한 이벤트 관리 테이블
    """
    event_uid = db.Column(db.String(256), primary_key=True)
    event_msg = db.Column(db.Text, nullable=False)
    channel_id = db.Column(db.String(256), nullable=False)
    create_date = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<event_uid %r, channel_id %r>' \
               % (self.event_uid, self.channel_id)


class ChannelInfo(db.Model):
    """
    특정 채널에서 발생한 이벤트를 어떤 채널을 통해 출력할지 관리.
    - 이벤트가 들어오는 inbound 채널(swing)과 이벤트를 출력할 outbound 채널(slack) 관리테이블
    - Slack 채널 ID 별 outbound 채널 설정
    """
    in_channel_id = db.Column(db.String(256), primary_key=True)
    out_channel_type = db.Column(db.String(1), primary_key=True)
    out_channel_id = db.Column(db.String(256), primary_key=True)
    out_channel_name = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return '<in_channel_id %r, out_channel_type %r, out_channel_id %r>' \
               % (self.in_channel_id, self.out_channel_type, self.out_channel_id)


class TargetList(db.Model):
    """
    Task 수행할 타겟 서버정보 관리 테이블.
    """
    task_id = db.Column(db.String(64), primary_key=True)
    host = db.Column(db.String(200), primary_key=True)  # enc
    port = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), primary_key=True)  # enc
    passwd = db.Column(db.String(200), nullable=False)  # enc
    out_channel_id = db.Column(db.String(256), primary_key=True)
    adapter_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<task_id %r, host %r, out_channel_id %r>' \
               % (self.task_id, self.host, self.out_channel_id)


class TaskList(db.Model):
    """
    Task 별 outbound 채널(slack) 관리 테이블.
    !현재 사용 안함.!
    """
    outbound_task_id = db.Column(db.String(64), primary_key=True)
    outbound_channel_id = db.Column(db.String(64), primary_key=True)

    def __repr__(self):
        return '<outbound_task_id %r, outbound_channel__id %r>' \
               % (self.outbound_task_id, self.outbound_channel_id)


class TaskInfo(db.Model):
    """
    Task 기본 정보 관리 테이블.
    """
    task_id = db.Column(db.String(64), primary_key=True)
    task_name = db.Column(db.String(512), primary_key=True)
    task_type = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.String(64), nullable=False)
    action_type = db.Column(db.String(1), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(16), nullable=False)
    update_time = db.Column(db.String(16), nullable=False)
    audit_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<task_id %r, task_name %r>' \
               % (self.task_id, self.task_name)


class TaskPlaybook(db.Model):
    """
    Task 상세 정보 관리 테이블.
    """
    task_id = db.Column(db.String(64), primary_key=True)
    task_seq = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text, nullable=False)
    cause = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.String(16), nullable=False)
    update_time = db.Column(db.String(16), nullable=False)
    audit_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<task_id %r, task_seq %r>' \
               % (self.task_id, self.task_seq)


class TaskManagement(db.Model):
    """
    Task별 User 관리 테이블.
    """
    owner_id = db.Column(db.String(64), primary_key=True)
    task_id = db.Column(db.String(64), primary_key=True)
    owner_type = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.String(16), nullable=False)
    update_time = db.Column(db.String(16), nullable=False)
    audit_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<owner_id %r, task_id %r>' \
               % (self.owner_id, self.task_id)


class WorkHistory(db.Model):
    """
    이벤트별 작업 이력 관리 테이블.
    """
    event_uid = db.Column(db.String(256), primary_key=True)
    outbound_task_id = db.Column(db.String(256), primary_key=True)
    exec_type = db.Column(db.String(1), nullable=True)
    create_date = db.Column(db.String(16), primary_key=True)

    def __repr__(self):
        return '<event_uid %r, outbound_task_id %r>' \
               % (self.event_uid, self.outbound_task_id)


class RecommendBaseInfo(db.Model):
    """
    추천 정보 테이블.
    """
    pattern_id = db.Column(db.String(126), primary_key=True)
    message_pattern = db.Column(db.Text, nullable=False)
    outbound_task_id = db.Column(db.String(256), nullable=False)
    call_cnt = db.Column(db.Integer, nullable=False)
    task_type = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return '<pattern_id %r, outbound_task_id %r, call_cnt %d>' \
               % (self.pattern_id, self.outbound_task_id, self.call_cnt)


class UserInfo(db.Model):
    """
    사용자 정보 관리 테이블.
    """
    user_id = db.Column(db.String(64), primary_key=True)
    user_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(200), primary_key=True)  # enc
    password = db.Column(db.String(200), nullable=False)  # enc
    status_code = db.Column(db.Integer, nullable=False)
    role_code = db.Column(db.Integer, nullable=False)
    slack_id = db.Column(db.String(128), nullable=True)
    create_time = db.Column(db.String(16), nullable=False)
    update_time = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return '<user_id %r, email %r>' \
               % (self.user_id, self.email)


class GroupInfo(db.Model):
    """
    그룹 정보 관리 테이블.
    """
    group_id = db.Column(db.String(64), primary_key=True)
    group_name = db.Column(db.String(256), primary_key=True)
    owner_id = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.String(16), nullable=False)
    update_time = db.Column(db.String(16), nullable=False)
    audit_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<group_id %r, group_name %r>' \
               % (self.group_id, self.group_name)


class GroupManagement(db.Model):
    """
    그룹 멤버 관리 테이블.
    """
    user_id = db.Column(db.String(64), primary_key=True)
    group_id = db.Column(db.String(64), primary_key=True)
    create_time = db.Column(db.String(16), nullable=False)
    update_time = db.Column(db.String(16), nullable=False)
    audit_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<user_id %r, group_id %r>' \
               % (self.user_id, self.group_id)
