# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class TestCsvMethods(unittest.TestCase):
    def test_event_data(self):
        """
        이벤트 데이터 수집.
        :return:
        """
        from trigger import Trigger

        trigger = Trigger()
        print(trigger.pick_event_data())
