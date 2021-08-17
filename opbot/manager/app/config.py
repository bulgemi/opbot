# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Config(object):
    """
    Manager 환경 설정 파일.
    """
    LOG_LEVEL = 'debug'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://db_id:db_password@localhost/db_name?charset=utf8'
    # RSA KEY
    PUBLIC_KEY = '/home/donghun/PycharmProjects/opbot_new/opbot/manager/pem/opbot_public.pem'
    PRIVATE_KEY = '/home/donghun/PycharmProjects/opbot_new/opbot/manager/pem/opbot_private.pem'
    # logging
    LOG_DIR_MANAGER = '/home/donghun/PycharmProjects/opbot_new/opbot/manager/logs'
    LOG_FORMAT_MANAGER = '%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s'
    LOG_LEVEL_MANAGER = DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_MANAGER = 'manager.log'
    # email
    MAIL_SUBJECT_PREFIX = "[OPBOT]"
    MAIL_SENDER = "OPBOT Admin <admin@opbot.com>"
    # 금지 명령어, 정규표현식 사용
    FORBIDDEN_INSTRUCTION = ['rm', 'kill', 'reboot']  # 'rm', 'kill', 'reboot'
