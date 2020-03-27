# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Manager 환경 설정 파일.
"""


class Config(object):
    LOG_LEVEL = 'debug'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://opbot_appl:apbot_appl26#!@localhost/opbot_db?charset=utf8'
    # RSA KEY
    PUBLIC_KEY = ''
    PRIVATE_KEY = ''
