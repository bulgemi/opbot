# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Analyzer 환경 설정 파일.
"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from celery.schedules import crontab


class Config(object):
    LOG_DIR = '/home/donghun/PycharmProjects/opbot/logs'
    LOG_LEVEL = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE = 'analyzer.log'
    LOG_FORMAT = '%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://opbot_appl:apbot_appl26#!@localhost/opbot_db?charset=utf8'
    DATASETS_DIR = '/home/donghun/datasets'


class Schedule(object):
    # Celery 환경 설정.
    CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours
    CELERY_TIMEZONE = 'Asia/Seoul'
    CELERY_ENABLE_UTC = False
    CELERYBEAT_SCHEDULE = {
        'channel-adapter': {
            'task': 'manage.task_channel_adapter',
            'schedule': crontab(minute='*/15')  # crontab(minute=30, hour=0)
        }
    }