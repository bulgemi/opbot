# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Config(object):
    SLACK_TOKEN = 'slack-token'

    LOG_DIR = '/home/donghun/PycharmProjects/opbot/logs'
    LOG_LEVEL_CHATBOT = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_CHATBOT = 'chatbot.log'
    LOG_LEVEL_ASYNCIO_RECEIVER = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_ASYNCIO_RECEIVER = 'asyncio_receiver.log'
    LOG_FORMAT = '%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s'

    RECOMMENDER_URI = "http://127.0.0.1:5959/api/1/events/"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://id:password@localhost/opbot_db?charset=utf8'
    # RSA KEY
    PRIVATE_KEY = '/home/donghun/PycharmProjects/opbot/opbot/manager/pem/opbot_private.pem'
