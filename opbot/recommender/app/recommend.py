# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
from difflib import SequenceMatcher
from operator import itemgetter
from sqlalchemy import and_
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import TaskInfo, RecommendBaseInfo


class Recommender(object):
    """
    알고리즘을 통한 분석/조치 태스크 추천
    """
    def __init__(self, db):
        """
        recommender 초기화.
        """
        self.__db = db

    def percentage_calc(self, total_sum, call_count):
        """
        테스크 추천도(백분율) 계산.
        소숫점 첫자리
        :param total_sum:
        :param call_count: 
        :return:
        """
        if total_sum == 0 or call_count == 0:
            return 0.0

        percentage = (float(call_count)/float(total_sum)) * 100.0
        return round(percentage, 1)

    def __get_task_info(self, action_type):
        """
        등록된 TASK 정보들을 반환.
        :param action_type:
        :return:
        """
        task_list = list()

        stmt = self.__db.session.query(TaskInfo)
        stmt = stmt.with_entities(TaskInfo.task_id)
        task_info = stmt.filter(TaskInfo.action_type == action_type.strip()).all()

        for task in task_info:
            task_list.append(task[0])
        return task_list

    def __get_recommend_base_info(self, event_msg, action_type):
        """
        ACTION TYPE 을 조회조건으로 event_msg 유사도가 90% 이상인 RECOMMEND_BASE_INFO 정보를 조회한다.
        :param event_msg:
        :param action_type:
        :return:
        """
        recommend_info = list()
        stmt = self.__db.session.query(RecommendBaseInfo)
        recommend_base_info = stmt.filter(RecommendBaseInfo.task_type == action_type.strip()).all()

        for rec in recommend_base_info:
            if self.__similarity_get(event_msg, rec.message_pattern) >= 0.90:
                recommend_info.append(rec)
        return recommend_info

    def recommend_info_get(self, event_msg, action_type='A'):
        """
        -분석('A')/조치('S')에 따라 TASK_INFO 테이블에서 action_type 별로 조회
        -조회된 TASK 를 기준으로 RECOMMEND_BASE_INFO 정보를 이용하여 백분율 계산 및 추천 순위 반환
        1.TASK_INFO 테이블에서 action_type 에 맞는 TASK ID LIST 조회
        2.event_msg 와 action_type 를 이용하여 패턴 유사도 90% 이상인 TASK 조회
        3.TASK ID의 존재 유무를 판단
        4.존재시 call_cnt 확인, 없으면 call_cnt = 0
        5.call_cnt 총합 계산
        6.TASK 별 추천도(백분율) 계산
        7.추천도를 기준으로 정렬
        :param event_msg:
        :param action_type:
        :return:
        """
        recommend_list = list()
        recommend_dict = dict()
        # 1.TASK_INFO 테이블에서 action_type 에 맞는 TASK ID LIST 조회
        tasks = self.__get_task_info(action_type)
        # 2.event_msg 와 action_type 를 이용하여 패턴 유사도 90% 이상인 TASK 조회
        recommend_info = self.__get_recommend_base_info(event_msg, action_type)
        # 3.TASK ID의 존재 유무를 판단
        # 4.존재시 call_cnt 확인, 없으면 call_cnt = 0
        for task in tasks:
            recommend_dict[task] = 0

        for rec in recommend_info:
            if rec.outbound_task_id in recommend_dict:
                recommend_dict[rec.outbound_task_id] = rec.call_cnt
        # 5.call_cnt 총합 계산
        total_call_cnt = sum(recommend_dict.values())
        # 6.TASK 별 추천도(백분율) 계산
        for key, value in recommend_dict.items():
            recommend_list.append({'task_id': key, 'percentage': self.percentage_calc(total_call_cnt, value)})
        # 7.추천도를 기준으로 정렬
        recommend_sorted = sorted(recommend_list, key=itemgetter('percentage'), reverse=True)

        return recommend_sorted

    def __similarity_get(self, a, b):
        """
        문장의 유사도 측정.
        :param a:
        :param b:
        :return:
        """
        return SequenceMatcher(None, a, b).ratio()
