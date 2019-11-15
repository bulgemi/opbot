# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
sys.path.append(os.getenv('OPBOT_HOME'))


class TestCollect(unittest.TestCase):
    def setUp(self) -> None:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from chatbot.app.config import Config
        from collector.app.collect import Collector

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 10,
            'pool_recycle': 500,  # bug-fix: MySQL server has gone away, my.conf: wait_timeout 보다 작아야 함.
            'pool_pre_ping': True
        }

        db = SQLAlchemy(app)

        self.__db = db
        self.__c = Collector(db)

    def test_001_action_info_add(self):
        self.__c.action_info_add('uid1234567890', 'task001', 'A')

    def test_002_action_info_get(self):
        self.__c.action_info_get('uid0987654321', 'task002', 'S')
