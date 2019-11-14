# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import unittest
sys.path.append(os.getenv('OPBOT_HOME'))


class TestAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        from flask_sqlalchemy import SQLAlchemy
        from analyzer.app import create_app

        app, manager, logger = create_app()
        db = SQLAlchemy(app)

        self.__app = app
        self.__manager = manager
        self.__logger = logger
        self.__db = db

    def tearDown(self) -> None:
        pass

    def test_001_(self):
        from analyzer.app.analysis import Analyzer

        analyzer = Analyzer(self.__db, self.__logger)
        self.assertTrue(analyzer.origin_dataset_generate())

    def test_002_csv(self):
        import csv
        with open('test.csv', 'w') as f:
            c = csv.writer(f, quoting=csv.QUOTE_ALL)
            c.writerow([1, 'a', 'abcd', 'ab"cd', "ab'cd", "ab,cd"])

    def test_003_similarity_get(self):
        from analyzer.app.analysis import Analyzer

        analyzer = Analyzer(self.__db, self.__logger)

        t01 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 75 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t02 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 112 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t03 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 75 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t04 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 85 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t05 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 94 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t06 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 90 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t07 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 66 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t08 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 68 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t09 = "[SWING TIMEOUT 발생] ZORDSCUS00700_TR01(KAIT부정가입방지 수신)업무에서 최근 3 분간 TIMEOUT 24 건 발생 - 담당자 김보현B(010 - 4588 - 8647)"
        t10 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 102 건 발생 - 담당자 권오성(010 - 9001 - 5059)"
        t11 = "[SWING TIMEOUT 발생] ZORDSSUBS0050_TR01(고객 서비스목록 조회)업무에서 최근 3 분간 TIMEOUT 115 건 발생 - 담당자 권오성(010 - 9001 - 5059)"

        print(analyzer.similarity_get(t01, t01))
        print(analyzer.similarity_get(t01, t02))
        print(analyzer.similarity_get(t01, t03))
        print(analyzer.similarity_get(t01, t04))
        print(analyzer.similarity_get(t01, t05))
        print(analyzer.similarity_get(t01, t06))
        print(analyzer.similarity_get(t01, t07))
        print(analyzer.similarity_get(t01, t08))
        print(analyzer.similarity_get(t01, t09))
        print(analyzer.similarity_get(t01, t10))
        print(analyzer.similarity_get(t01, t11))

    def test_004_read_csv(self):
        import csv

        with open('/home/donghun/datasets/A/origin_20191113.csv', 'r') as csvfile:
            spam_reader = csv.reader(csvfile)
            for row in spam_reader:
                print(row)

    def test_005_grouping(self):
        from analyzer.app.analysis import Analyzer

        analyzer = Analyzer(self.__db, self.__logger)
        self.assertTrue(analyzer.dataset_grouping('20191113'))

    def test_006_classfy(self):
        from analyzer.app.analysis import Analyzer

        analyzer = Analyzer(self.__db, self.__logger)
        self.assertTrue(analyzer.dataset_classfy('20191113'))

    def test_007_adding(self):
        from analyzer.app.analysis import Analyzer

        analyzer = Analyzer(self.__db, self.__logger)
        self.assertTrue(analyzer.dataset_adding('20191113'))
