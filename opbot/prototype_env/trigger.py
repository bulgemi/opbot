# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import csv
import time
import os


class Trigger(object):
    def __init__(self):
        self.__csv_file = '/home/donghun/PycharmProjects/opbot/opbot/prototype_env/tp_timeout.csv'
        self.__pick_info = "/home/donghun/PycharmProjects/opbot/opbot/prototype_env/event.pick"
        self.__event_data = None

    def __read_line(self):
        try:
            with open(self.__csv_file) as csv_fp:
                spam_reader = csv.reader(csv_fp)

                for index, row in enumerate(spam_reader):
                    if index != 0:
                        yield row
        except FileNotFoundError:
            print("File Not Found Error: %s" % self.__csv_file)
            raise FileExistsError

    def __make_event_data(self, row):
        """
        tp timeout 이벤트 데이터 가공
        :param row:
        :return:
        """
        try:
            cur_time = time.localtime(time.time())
            time1 = time.strftime('%Y-%m-%d %H:%M', cur_time)
            time2 = time.strftime('%Y%m%d%H%M', cur_time)

            row = [x.strip() for x in row]

            edit_info = {
                5: time1,
                6: time2,
                15: time1,
            }

            for index in edit_info:
                row[index] = edit_info[index]

            self.__event_data = row
        except Exception:
            print("Failed make event data!")
            raise Exception

    def __pick_num(self):
        """
        row num 정보 파일.
        :return:
        """
        if os.path.exists(self.__pick_info) is True:
            pick_num = None

            with open(self.__pick_info, 'r') as pick:
                tmp = pick.read()

                if tmp == '':
                    pick_num = 0
                else:
                    pick_num = int(tmp)
                print("%d" % pick_num)

            pick_num += 1

            with open(self.__pick_info, 'w') as pick:
                pick.write(str(pick_num))
            return pick_num
        else:
            with open(self.__pick_info, 'w') as pick:
                pick.write("0")
            return 0

    def __reset_pick(self):
        """
        row num 초기화
        :return:
        """
        with open(self.__pick_info, 'w') as pick:
            pick.write("0")

    def __pick(self):
        """
        tp timeout 이벤트 데이터 반환.
        :return:
        """
        data_list = self.__read_line()
        pick_num = self.__pick_num()

        for index, data in enumerate(data_list):
            if index == pick_num:
                # print(data)
                self.__make_event_data(data)
                return self.__event_data

    def pick_event_data(self):
        data = self.__pick()

        if data is None:
            self.__reset_pick()
            data = self.__pick()
        return data
