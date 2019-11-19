# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'


class Recommender(object):
    """
    알고리즘을 통한 분석/조치 태스크 추천
    """
    def __init__(self):
        """
        recommender 초기화.
        """
        pass

    def percentage_calc(self):
        """
        테스크 추천도(백분율) 계산.
        :return:
        """
        pass

    def task_sort(self):
        """
        추천도(백분율)에 따라 테스크 정렬.
        :return:
        """
        pass

    def task_recommend(self):
        """
        추천도가 가장 높은 태스크 반환.
        :return:
        """
        pass

    def recommend_info_get(self):
        """
        -분석('A')/조치('S')에 따라 TASK_INFO 테이블에서 action_type 별로 조회
        -조회된 TASK 를 기준으로 RECOMMEND_BASE_INFO 정보를 이용하여 백분율 계산 및 추천 순위 반환
        :return:
        """
        pass
