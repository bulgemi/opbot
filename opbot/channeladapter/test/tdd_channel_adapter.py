# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
sys.path.append(os.getenv('OPBOT_HOME'))


class TestChannelAdapter(unittest.TestCase):
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

    def test_channel_adapter_notify_all(self):
        from channeladapter.app.channel_adapter import ChannelAdapter
        from channeladapter.app.adapter.adapter_oracle import AdapterOracle

        channel_adapter = ChannelAdapter(self.db, self.logger)
        adapter = AdapterOracle(channel_adapter)
        channel_adapter.attach(adapter)
        channel_adapter.notify_all()

    def test_create_channel_adapter(self):
        from channeladapter.app.channel_adapter import ChannelAdapter

        channel_adapter = ChannelAdapter(self.db, self.logger)

        print(channel_adapter)

    def test_logger(self):
        self.logger.debug("test logging!")
        self.logger.debug("%r" % os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

    def test_channel_adapter_call_rest_api(self):
        from channeladapter.app.channel_adapter import ChannelAdapter

        channel_adapter = ChannelAdapter(self.db, self.logger)

        print(channel_adapter.call_rest_api('channel_id', 'msg'))

    def test_channel_adapter_add_history(self):
        import uuid
        import time
        from channeladapter.app.channel_adapter import ChannelAdapter
        from manager.app.models import EventHistory

        cur_time = time.localtime(time.time())
        channel_adapter = ChannelAdapter(self.db, self.logger)
        event_history = EventHistory()

        event_history.channel_id = 'test_channel_01'
        event_history.event_uid = str(uuid.uuid4())
        event_history.event_msg = "한글, english, 1234, !@$#"
        event_history.create_date = time.strftime('%Y%m%d%H%M%S', cur_time)
        channel_adapter.add_history(event_history)
