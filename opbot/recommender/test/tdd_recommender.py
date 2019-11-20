# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
sys.path.append(os.getenv('OPBOT_HOME'))


class TestRecommend(unittest.TestCase):
    def setUp(self) -> None:
        from flask_sqlalchemy import SQLAlchemy
        from recommender.app import create_app

        app, manager = create_app()
        db = SQLAlchemy(app)

        self.__app = app
        self.__manager = manager
        self.__db = db

    def tearDown(self) -> None:
        pass

    def test_001_percentage_calc(self):
        from recommender.app.recommend import Recommender

        recomm = Recommender(self.__db)

        self.assertEqual(recomm.percentage_calc(100, 20), 20.0)
        self.assertEqual(recomm.percentage_calc(100, 33), 33.0)
        self.assertEqual(recomm.percentage_calc(100, 34), 34.0)
        self.assertEqual(recomm.percentage_calc(100, 35), 35.0)
        self.assertEqual(recomm.percentage_calc(100, 0), 0.0)

        print(recomm.percentage_calc(100, 0))
        print(recomm.percentage_calc(100, 24))
        print(recomm.percentage_calc(100, 16))
        print(recomm.percentage_calc(100, 10))
        print(recomm.percentage_calc(100, 50))

    def test_002_recommend_info_get(self):
        from recommender.app.recommend import Recommender

        recomm = Recommender(self.__db)

        event_msg = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3분간 TIMEOUT 90건 발생 - 담당자 권오성(010-9001-5059)"
        print(recomm.recommend_info_get(event_msg))
        print(recomm.recommend_info_get(event_msg, 'S'))
