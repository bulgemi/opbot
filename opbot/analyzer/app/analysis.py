# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
import csv
from uuid import uuid1
from difflib import SequenceMatcher
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from .config import Config
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import WorkHistory, EventHistory, RecommendBaseInfo


class Analyzer(object):
    def __init__(self, db, logger):
        self.__db = db
        self.__logger = logger
        self.__datasets_dir = Config.DATASETS_DIR

    def origin_dataset_generate(self):
        """
        학습 데이터 dataset 가공을 위한 원천 dataset 생성.
        1.origin dataset 파일(CSV) 파일 생성
        -분석('A')/조치('S') 별 파일 생성
        -파일명: origin_YYYYMMDD.csv
        2.work_history 조회.
        3.event message 조회
        4.분석/조치 별 csv 파일 생성.
        :return:
        """
        today = datetime.now().strftime("%Y%m%d")

        a_csv = open("{0}/A/origin_{1}.csv".format(self.__datasets_dir, today), 'w')
        s_csv = open("{0}/S/origin_{1}.csv".format(self.__datasets_dir, today), 'w')

        a = csv.writer(a_csv, quoting=csv.QUOTE_ALL)
        s = csv.writer(s_csv, quoting=csv.QUOTE_ALL)

        try:
            history_info = self.__work_history_get(today)

            for history in history_info:
                event_uid = history[0]
                exec_type = history[1]
                task_id = history[2]

                event_message = self.__event_message_get(event_uid)

                if exec_type == 'A':
                    a.writerow([event_message, task_id, exec_type])
                elif exec_type == 'S':
                    s.writerow([event_message, task_id, exec_type])
                else:
                    pass
        except SQLAlchemyError as e:
            self.__logger.error("!%r!" % str(e.orig))
            return False
        except BaseException as e:
            self.__logger.error("!%r!" % str(e.orig))
            return False
        finally:
            # self.__logger.debug("!!! close csv files.")
            a_csv.close()
            s_csv.close()
        return True

    def dataset_pre_proc(self):
        """
        원천 dataset 을 기반으로 학습 데이터 dataset 생성.
        :return:
        """
        pass

    def __work_history_get(self, create_date):
        """
        work_history table 에서 이력 정보 수집.
        :param create_date:
        :return:
        """
        # todo: work_history 조회 성능 문제시 튜닝필요.
        stmt = self.__db.session.query(WorkHistory)
        stmt = stmt.with_entities(WorkHistory.event_uid,
                                  WorkHistory.exec_type,
                                  WorkHistory.outbound_task_id)
        work_history_info = stmt.filter(WorkHistory.create_date.like("{}%".format(create_date.strip()))).all()
        return work_history_info

    def __event_message_get(self, event_uid):
        """
        uid 를 이용하여 event message 조회.
        :param event_uid:
        :return:
        """
        stmt = self.__db.session.query(EventHistory)
        stmt = stmt.with_entities(EventHistory.event_msg)
        event_message = stmt.filter(EventHistory.event_uid == event_uid.strip()).first()
        return event_message[0]

    def recommend_renew(self):
        """
        추천 수치 갱신.
        :return:
        """
        pass

    def __grouping(self, create_date, t='A'):
        """
        1.read an origin csv
        2.row 분석, 컬럼 갯수 확인(3개?, 4개?)
        -3개일 경우: 신규 row, 첫번째 row 일 경우 0 번째 항목 pattern 등록
        -4개일 경우: grouping 완료된 row, skip
        3.row 0 번째 항목의 유사도를 측정하여, 90% 이상일 경우 grouping csv 파일에 추가
        :param create_date:
        :param t:
        :return:
        """
        p = 'group'
        file_name = "{}.csv".format(str(uuid1()))
        o_csv = "{0}/{1}/origin_{2}.csv".format(self.__datasets_dir, t, create_date)
        tmp_name = "{0}/{1}/origin_{2}.tmp".format(self.__datasets_dir, t, create_date)
        t_csv = open(tmp_name, 'w')
        tf = csv.writer(t_csv, quoting=csv.QUOTE_ALL)

        with open(o_csv, 'r') as csvfile:
            pattern_temp = ""
            row_num = 0
            spam_reader = csv.reader(csvfile)

            # 디렉토리 생성
            if not os.path.isdir("{0}/{1}/{2}/{3}".format(self.__datasets_dir, t, p, create_date)):
                os.makedirs("{0}/{1}/{2}/{3}".format(self.__datasets_dir, t, p, create_date))

            new_file_name = "{0}/{1}/{2}/{3}/{4}".format(self.__datasets_dir,
                                                         t, p, create_date, file_name)

            n_file = open(new_file_name, "w")
            nf = csv.writer(n_file, quoting=csv.QUOTE_ALL)

            for row in spam_reader:
                tmp_list = [x for x in row]

                if len(row) < 4:  # 신규
                    if row_num == 0:
                        pattern_temp = row[0]
                        nf.writerow(row)
                    else:
                        if self.similarity_get(pattern_temp, row[0]) >= 0.90:
                            nf.writerow(row)
                    if row is not None:
                        tmp_list.append('Y')
                        tf.writerow(tmp_list)
                    row_num += 1
                else:  # 분석 완료
                    tf.writerow(tmp_list)
        # tmp, csv 교체
        t_csv.close()

        if os.path.isfile(o_csv):
            os.remove(o_csv)
            os.rename(tmp_name, o_csv)

        return True

    def __classify(self, create_date, t='A'):
        """
        grouping csv 파일을 TASK ID 별로 분류한다.
        :param create_date:
        :param t:
        :return:
        """
        p = 'classify'
        g_dir = "{0}/{1}/group/{2}".format(self.__datasets_dir, t, create_date)
        f_list = os.listdir(g_dir)
        task_map = dict()

        for f in f_list:
            g_csv = "{0}/{1}".format(g_dir, f)

            with open(g_csv, 'r') as csvfile:
                spam_reader = csv.reader(csvfile)

                for row in spam_reader:
                    # TASK ID별 파일 생성.
                    if row[1] not in task_map:
                        if not os.path.isdir("{0}/{1}/{2}/{3}".format(self.__datasets_dir, t, p, create_date)):
                            os.makedirs("{0}/{1}/{2}/{3}".format(self.__datasets_dir, t, p, create_date))

                        file_name = "{0}/{1}/{2}/{3}/{4}.csv".format(self.__datasets_dir,
                                                                     t, p, create_date, str(uuid1()))
                        n_file = open(file_name, "w")
                        nf = csv.writer(n_file, quoting=csv.QUOTE_ALL)
                        task_map[row[1]] = [n_file, nf]
                    # 파일 내용 쓰기.
                    tmp_tf = task_map[row[1]][1]
                    tmp_tf.writerow(row)
        # close the files
        for k, v in task_map.items():
            v[0].close()

        return True

    def dataset_grouping(self, create_date):
        """
        1.Grouping
        -Origin CSV 내 오류 메시지의 유사도가 90%이상인 row 끼리 그룹핑
        -파일명: 'A' or 'S'/group/YYYYMMDD/{uuid}.csv
        :param create_date:
        :return:
        """
        self.__grouping(create_date, 'A')
        self.__grouping(create_date, 'S')

        return True

    def dataset_classify(self, create_date):
        """
        2.Classify
        -그룹 csv 파일을 read 하여 TASK ID 별로 분류한다.
        -파일명: 'A' or 'S'/classify/YYYYMMDD/{uuid}.csv
        :param create_date:
        :return:
        """
        self.__classify(create_date, 'A')
        self.__classify(create_date, 'S')

        return True

    def __adding(self, create_date, t='A'):
        """
        1.classify 디렉토리에 생성된 csv 파일 read
        2.recommend_base_info table 에 유사도가 90%이상이고 TASK ID가 동일한 row 존재시 call_cnt +1 증가.
        3.row 없을 경우, row 추가 후 call_cnt +1 증가
        :param create_date:
        :param t:
        :return:
        """
        c_dir = "{0}/{1}/classify/{2}".format(self.__datasets_dir, t, create_date)

        try:
            f_list = os.listdir(c_dir)

            for f in f_list:
                c_csv = "{0}/{1}".format(c_dir, f)

                with open(c_csv, 'r') as csvfile:
                    spam_reader = csv.reader(csvfile)

                    for row in spam_reader:
                        insert_flag = True
                        stmt = self.__db.session.query(RecommendBaseInfo)
                        recommend_base_rows = stmt.all()
                        # recommend_base_info 데이터 비교
                        for recommend_base_row in recommend_base_rows:
                            if self.similarity_get(row[0], recommend_base_row.message_pattern) >= 0.90 \
                                    and row[1] == recommend_base_row.outbound_task_id:
                                insert_flag = False
                                recommend_base_row.call_cnt += 1

                                self.__db.session.add(recommend_base_row)
                                self.__db.session.commit()
                        # insert_flag 가 True 이면 add new row
                        if insert_flag is True:
                            insert_row = RecommendBaseInfo()

                            insert_row.pattern_id = str(uuid1())
                            insert_row.message_pattern = row[0]
                            insert_row.outbound_task_id = row[1]
                            insert_row.call_cnt = 1  # call_cnt 1
                            insert_row.task_type = t

                            self.__db.session.add(insert_row)
                            self.__db.session.commit()
                        insert_flag = True
        except SQLAlchemyError as e:
            self.__logger.error("!%r!" % str(e))
            self.__db.session.rollback()
            return False
        except FileNotFoundError:
            return True
        except BaseException as e:
            self.__logger.error("!%r!" % str(e))
            return False
        return True

    def dataset_adding(self, create_date):
        """
        3.Adding
        -classify csv 파일 row의 오류 메시지가 RECOMMEND_INFO 테이블에 MESSAGE_PATTERN 컬럼 데이터와 유사도 90%일 경우
         OUTBOUND_TASK_ID 없으면 INSERT 존재하면 CALL_CNT 1 증가
        :param create_date:
        :return:
        """
        self.__adding(create_date, 'A')
        self.__adding(create_date, 'S')

        return True

    def similarity_get(self, a, b):
        """
        문장의 유사도 측정.
        :param a:
        :param b:
        :return:
        """
        return SequenceMatcher(None, a, b).ratio()
