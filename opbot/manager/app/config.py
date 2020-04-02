# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
"""
Manager 환경 설정 파일.
"""


class Config(object):
    LOG_LEVEL = 'debug'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://opbot_appl:apbot_appl26#!@localhost/opbot_db?charset=utf8'
    # RSA KEY
    PUBLIC_KEY = '/home/donghun/PycharmProjects/opbot/opbot/manager/pem/opbot_public.pem'
    PRIVATE_KEY = '/home/donghun/PycharmProjects/opbot/opbot/manager/pem/opbot_private.pem'
    # logging
    LOG_DIR_MANAGER = '/home/donghun/PycharmProjects/manager/logs'
    LOG_FORMAT_MANAGER = '%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s'
    LOG_LEVEL_MANAGER = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_MANAGER = 'manager.log'
