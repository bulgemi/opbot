# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Observer 디자인 패턴 적용.
"""
import sys
import os
from datetime import date, datetime, timedelta
from abc import ABCMeta, abstractmethod
from sqlalchemy.exc import SQLAlchemyError
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import EventHistory


class ChannelAdapter(object):
    def __init__(self, db, logger):
        self.__observers = []
        self.__conn = None
        self.__db = db
        self.logger = logger

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

    def notify_all(self):
        """
        정보 수집 후 알림.
        :return:
        """
        import time
        import requests

        for observer in self.__observers:
            channel_id, uid_set, msg_dict = observer.scrape(self)
            new_events = self.catch_event(uid_set)

            self.logger.debug("new_events-><%r>" % new_events)

            for new_event in new_events:
                # save history
                event_history = EventHistory()

                event_history.channel_id = channel_id
                event_history.event_uid = new_event
                event_history.event_msg = msg_dict[new_event]
                cur_time = time.localtime(time.time())
                event_history.create_date = time.strftime('%Y%m%d%H%M%S', cur_time)

                # notify
                try:
                    self.add_history(event_history)
                    observer.notify(self, channel_id, msg_dict[new_event], new_event)
                except requests.exceptions.RequestException as e:
                    self.logger.error("!%s!" % e)
                    pass
                except SQLAlchemyError as e:
                    self.logger.error("!%s!" % e)
                    pass

    def call_rest_api(self, channel_id, msg, msg_uid):
        import requests
        """
        REST API 호출
        :param channel_id:
        :param msg:
        :param msg_uid:
        :return:
        """
        api_host = "http://127.0.0.1:9595/api/1/events/"
        data = {'channel_id': channel_id,
                'event_msg': msg,
                'event_uid': msg_uid}

        self.logger.debug("data=<%r>" % data)

        try:
            r = requests.post(api_host, json=data)
            return r
        except requests.exceptions.RequestException as e:
            self.logger.error("!%s!" % e)
            raise e

    def add_history(self, event_info):
        """
        insert event_history
        :param event_info: EventHistory Object
        :return:
        """
        try:
            self.__db.session.add(event_info)
            self.__db.session.commit()
        except SQLAlchemyError as e:
            self.logger.error("!%r!" % str(e.orig))
            self.__db.session.rollback()
            raise e

    def catch_event(self, channel_event_set):
        """
        이벤트 존재 유무 감지.
        :param channel_event_set: channel 이벤트 리스트 집합
        :return:
        """
        # Todo : 'EventHistory' 테이블 조회 부분 개선 여부 확인
        day1 = "{}%".format(datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d'))
        day2 = "{}%".format(datetime.strftime(datetime.now(), '%Y%m%d'))

        stmt = self.__db.session.query(EventHistory).with_entities(EventHistory.event_uid)
        b = stmt.filter(EventHistory.create_date.like(day1) | EventHistory.create_date.like(day2)).all()
        set_b = set([x[0] for x in b])

        self.logger.debug("channel_event_set-><%r>" % channel_event_set)
        self.logger.debug("set_b-><%r>" % set_b)

        return channel_event_set - set_b


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
        channel 정보 수집
        :return:
        """
        pass
