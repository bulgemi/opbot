# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Observer 디자인 패턴 적용.
"""
from abc import ABCMeta, abstractmethod


class ChannelAdapter(object):
    def __init__(self):
        self.__observers = []
        self.__conn = None

    def attach(self, observer):
        """
        채널 등록
        :param observer:
        :return:
        """
        self.__observers.append(observer)

    def detach(self):
        """
        채널 제거
        :return:
        """
        self.__observers.pop()

    def connect(self, conn):
        """
        채널 연결
        :param conn:
        :return:
        """
        self.__conn = conn

    def notify_all(self):
        """
        정보 수집 후 알림.
        :return:
        """
        for observer in self.__observers:
            channel_id, event_message = observer.scrape(self)
            observer.notify(self, channel_id, event_message)


class Adapter(metaclass=ABCMeta):
    @abstractmethod
    def notify(self):
        """
        이벤트 REST API 호출.
        :return:
        """
        pass

    @abstractmethod
    def scrape(self):
        """
        정보 수집, EVENT_HISTORY Insert/Update
        :return:
        """
        pass
