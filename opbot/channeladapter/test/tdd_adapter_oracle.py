# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
sys.path.append(os.getenv('OPBOT_HOME'))


class TestAdapterOracle(unittest.TestCase):
    def setUp(self) -> None:
        import logging
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_script import Manager
        from channeladapter.app.config import Config

        app = Flask(__name__)
        # charset=utf8 설정 중요!
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        manager = Manager(app)
        logging.basicConfig(filename=Config.LOG_FILE,
                            level=Config.LOG_LEVEL,
                            format='%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s')

        self.app = app
        self.manager = manager
        self.logger = logging
        self.db = db

    def tearDown(self) -> None:
        pass

    def test_init_adatper(self):
        from channeladapter.app.channel_adapter import ChannelAdapter
        from channeladapter.app.adapter.adapter_oracle import AdapterOracle

        channel_adapter = ChannelAdapter(self.db, self.logger)
        adapter = AdapterOracle(channel_adapter)

        print(adapter)

    def test_scrape(self):
        from channeladapter.app.channel_adapter import ChannelAdapter
        from channeladapter.app.adapter.adapter_oracle import AdapterOracle

        channel_adapter = ChannelAdapter(self.db, self.logger)
        adapter = AdapterOracle(channel_adapter)
        tmp = adapter.scrape(channel_adapter)
        print(tmp)

    def test_catch_event(self):
        from channeladapter.app.channel_adapter import ChannelAdapter
        from channeladapter.app.adapter.adapter_oracle import AdapterOracle

        channel_adapter = ChannelAdapter(self.db, self.logger)
        adapter = AdapterOracle(channel_adapter)
        tmp = adapter.scrape(channel_adapter)

        event_list = channel_adapter.catch_event(tmp)
        print(event_list)
