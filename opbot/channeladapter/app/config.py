# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Channel Adapter 환경 설정 파일.
"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from datetime import timedelta


class Config(object):
    LOG_LEVEL = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE = 'channel_adapter.log'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://db_id:db_password@localhost/db_name?charset=utf8'


class AdapterOracle(object):
    HOST = 'localhost'
    USER = 'pm_svc'
    PASSWORD = '!pm1svc'
    DB = 'oracle_db'


class Schedule(object):
    # Celery 환경 설정.
    CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours
    CELERY_TIMEZONE = 'Asia/Seoul'
    CELERY_ENABLE_UTC = False
    CELERYBEAT_SCHEDULE = {
        'channel-adapter': {
            'task': 'manage.task_channel_adapter',
            'schedule': timedelta(seconds=10)
        }
    }
