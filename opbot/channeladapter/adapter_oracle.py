# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Oracle DB Adapter
"""


class AdapterOracle(object):
    def __init__(self, channel_adapter):
        """
        채널 등록, 채널 연결
        :param channel_adapter:
        """
        channel_adapter.attach(self)

    def notify(self, channel_adapter, channel_id, event_message):
        """
        Chatbot REST API 호출
        :param channel_adapter:
        :param channel_id:
        :param event_message:
        :return:
        """
        pass

    def scrape(self, channel_adapter):
        """
        정보 수집, EVENT_HISTORY Insert/Update
        :param channel_adapter:
        :return:
        """
        pass
