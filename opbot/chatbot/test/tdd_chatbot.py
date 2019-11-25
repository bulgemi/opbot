# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
sys.path.append(os.getenv('OPBOT_HOME'))


class TestChatBot(unittest.TestCase):
    def setUp(self) -> None:
        from flask_sqlalchemy import SQLAlchemy
        from chatbot.app import create_app

        app, manager = create_app()
        db = SQLAlchemy(app)

        self.app = app
        self.manager = manager
        self.db = db

    def tearDown(self) -> None:
        pass

    def test_001_channel_read(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)
        result = chatbot.channel_read('swing')
        if len(result) > 0:
            for channel_info in result:
                print(channel_info)

        result = chatbot.channel_read('xx')
        if len(result) > 0:
            for channel_info in result:
                print(channel_info)

    def test_002_put_broadcast(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)

        message = "[SWING TIMEOUT 발생] ZORDSCUS00700_TR01(KAIT부정가입방지 수신)업무에서 최근 3분간 TIMEOUT 24건 발생"\
                  " - 담당자 김보현B(010-4588-8647)"
        chatbot.put_broadcast(channel='#swing', message=message)

    def test_005_parse_command(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)

        self.assertEqual(chatbot.parse_command(""), [])
        self.assertEqual(chatbot.parse_command("aaaaaaaa"), [])
        self.assertEqual(chatbot.parse_command("1234567890"), [])
        self.assertEqual(chatbot.parse_command("가나다라마바사"), [])
        self.assertEqual(chatbot.parse_command("1.a"), [])
        self.assertEqual(chatbot.parse_command("1.가"), [])
        self.assertEqual(chatbot.parse_command("!1!"), ["!1!"])
        self.assertEqual(chatbot.parse_command("!aaa!"), ["!aaa!"])
        self.assertEqual(chatbot.parse_command("!한글!"), ["!한글!"])
        self.assertEqual(chatbot.parse_command("!1.한글!"), ["!1.한글!"])
        self.assertEqual(chatbot.parse_command("!1!!2!"), ["!1!", "!2!"])
        self.assertEqual(chatbot.parse_command("!aaa!!bbb!"), ["!aaa!", "!bbb!"])
        self.assertEqual(chatbot.parse_command("!한글!!글한!"), ["!한글!", "!글한!"])
        self.assertEqual(chatbot.parse_command("!a!aaa!aaa"), ["!a!"])
        self.assertEqual(chatbot.parse_command("!aa!aaaaaa"), ["!aa!"])
        self.assertEqual(chatbot.parse_command("aaaaa!a!"), ["!a!"])
        self.assertEqual(chatbot.parse_command("!TP_상태_분석!"), ["!TP_상태_분석!"])

    def test_006_subjects(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)

        chatbot.set_current_subjects("#test_out_channel", "abc123!")
        self.assertEqual(chatbot.get_current_subjects("#test_out_channel"), "abc123!")

    def test_007_subjects(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)

        chatbot.del_current_subjects("#test_out_channel")
        self.assertIsNone(chatbot.get_current_subjects("#test_out_channel"))

    def test_008_context(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)

        chatbot.set_context_a("#test_out_channel", "abc123!")
        self.assertEqual(chatbot.get_context("#test_out_channel", "abc123!"), "A")
        chatbot.set_context_s("#test_out_channel", "abc123!")
        self.assertEqual(chatbot.get_context("#test_out_channel", "abc123!"), "S")

    def test_009_context(self):
        from chatbot.app.bot import ChatBot

        chatbot = ChatBot(self.db)

        chatbot.del_context("#test_out_channel", "abc123!")
        self.assertEqual(chatbot.get_context("#test_out_channel", "abc123!"), "A")
