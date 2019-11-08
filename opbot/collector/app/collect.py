# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import WorkHistory


class Collector(object):
    """
    사용자 이벤트 수집기
    """
    def __init__(self, db):
        self.__db = db

    def action_info_get(self, event_uid, task_id):
        """
        사용자 이벤트 수집.
        :param event_uid:
        :param task_id:
        :return:
        """
        return self.action_info_add(event_uid, task_id)

    def action_info_add(self, event_uid, task_id):
        """
        사용자 이벤트 저장.
        WorkHistory table 에 사용자 이벤트 데이터 저장.
        :param event_uid: 
        :param task_id: 
        :return:
        """
        now = datetime.now()

        work_history = WorkHistory()
        work_history.event_uid = event_uid
        work_history.outbound_task_id = task_id
        work_history.create_date = now.strftime('%Y%m%d%H%M%S')  # create_date, YYYYmmddHHMMSS

        try:
            self.__db.session.add(work_history)
            self.__db.session.commit()
        except SQLAlchemyError as e:
            self.__db.session.rollback()
            raise e
        return True
