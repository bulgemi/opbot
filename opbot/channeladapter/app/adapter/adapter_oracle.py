# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
Oracle DB Adapter
"""
import sys
import os
import pymysql
from datetime import date, datetime, timedelta
sys.path.append(os.getenv('OPBOT_HOME'))


class AdapterOracle(object):
    def __init__(self, channel_adapter):
        """
        채널 등록, 채널 연결
        :param channel_adapter:
        """
        from channeladapter.app.config import AdapterOracle

        try:
            # Connect to the database
            connection = pymysql.connect(host=AdapterOracle.HOST,
                                         user=AdapterOracle.USER,
                                         password=AdapterOracle.PASSWORD,
                                         db=AdapterOracle.DB,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

            self.__conn = connection

            channel_adapter.logger.debug("Success Connect DB.")
        except pymysql.MySQLError as e:
            channel_adapter.logger.error("Failed Connect DB!(%r)" % e)

            sys.exit()

        channel_adapter.attach(self)

    def __del__(self):
        """
        채널 연결 종료.
        :return:
        """
        self.__conn.close()
        # print("disconnect db.")

    def notify(self, channel_adapter, channel_id, event_message):
        """
        Chatbot REST API 호출
        :param channel_adapter:
        :param channel_id:
        :param event_message:
        :return:
        """
        import requests

        try:
            channel_adapter.call_rest_api(channel_id, event_message)
        except requests.exceptions.RequestException as e:
            raise e

    def scrape(self, channel_adapter):
        """
        Oracle 이벤트 정보 수집
        :param channel_adapter:
        :return: channel_id, uid_set, msg_dict
        """
        day1 = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
        day2 = datetime.strftime(datetime.now(), '%Y%m%d')

        sql = " select log_num, service_id, msg from pm_svc_log_mon "\
              " where issue_receive_date like '{0}%%' "\
              " or issue_receive_date like '{1}%%' ".format(day1, day2)

        channel_adapter.logger.debug("sql=<%r>" % sql)

        try:
            with self.__conn.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()

                channel_adapter.logger.debug("results=<%r>" % results)
        except pymysql.MySQLError as e:
            channel_adapter.logger.error("Error: %r" % e)
            return None

        key_list = list()
        msg_dict = dict()

        for x in results:
            key_list.append(x['log_num'] + x['service_id'])
            msg_dict[x['log_num'] + x['service_id']] = x['msg']
        # event_uid 집합 생성, event_uid 는 채널에 맞게 생성.
        return 'swing', set(key_list), msg_dict
