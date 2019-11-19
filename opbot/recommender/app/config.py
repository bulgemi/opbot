# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Config(object):
    LOG_DIR = '/home/donghun/PycharmProjects/opbot/logs'
    LOG_LEVEL = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE = 'recommender.log'
    LOG_FORMAT = '%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://opbot_appl:apbot_appl26#!@localhost/opbot_db?charset=utf8'
