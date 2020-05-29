# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import csv
import pandas as pd
from .datapreprocessor import DataPreprocessor


class Step2(DataPreprocessor):
    def do_type0(self, f_msg, o_msg):
        if f_msg.find("●서버:") != -1:
            l_tmp = f_msg.split("●서버:")
            self.key_value = self.data_filter(l_tmp[1])

        if f_msg.find("●메시지:") != -1:
            l_tmp = f_msg.split("●메시지:")
            self.key_value += self.data_filter(l_tmp[1])

        self.contents.append(o_msg)
        return

    def do_type2(self, f_msg, o_msg):
        if f_msg.find("●내용:") != -1:
            l_tmp = f_msg.split("●내용:")
            self.key_value = self.data_filter(l_tmp[1])
        self.contents.append(o_msg)
        return

    def do_type3(self, f_msg, o_msg):
        if f_msg.find("●내용:") != -1:
            l_tmp = f_msg.split("●내용:")
            self.key_value = self.data_filter(l_tmp[1])
        elif f_msg.find("●장애현상:") != -1:
            l_tmp = f_msg.split("●장애현상:")
            self.key_value = self.data_filter(l_tmp[1])
        else:
            pass
        self.contents.append(o_msg)
        return

    def read_xls(self):
        for i, r in self.data.iterrows():
            if pd.isnull(self.get_type(r)):
                pass
            else:
                if len(self.contents) > 0:
                    self.find_contents()
                self.type = self.key_map[self.get_type(r)]
                self.measure = False
                self.s_close = False
                self.contents.clear()
                self.time_stamp = "{}".format(int(r['문자발송일시']))

            send_message = self.get_send_message(r)

            if self.type == 1 or pd.isnull(send_message):
                pass
            else:
                s_tmp = str(send_message).replace(" ", "")
                if self.type == 0:
                    self.do_type0(s_tmp, send_message)
                elif self.type == 2:
                    self.do_type2(s_tmp, send_message)
                elif self.type == 3:
                    self.do_type3(s_tmp, send_message)
                else:
                    pass

        return True

    def find_contents(self):
        import os

        save_dir = "/datapreprocessor/data/preprocess_data/{}/".format(self.type)
        tmp = ""
        idx = 0
        for s in self.key_value:
            tmp += s
            if idx == 50:
                tmp += '/'
                idx = 0
            idx += 1
        full_path = os.getenv('OPBOT_HOME') + save_dir + tmp + "/r.txt"
        # print(full_path)
        # print("ts(%s)=%r" % (type(self.time_stamp), self.time_stamp))
        try:
            f = open(full_path, 'r')
            line = f.readline()
            self.write_csv(line)
            f.close()
        except OSError as e:
            self.write_csv('')

    def create_csv(self):
        import os
        self.fp = open(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/Rims_result.csv", 'w')
        self.csv_fp = csv.writer(self.fp, delimiter=',')

    def close_csv(self):
        self.fp.close()

    def write_csv(self, result):
        key_map = {0: "통합품질감시", 1: "장애의심", 2: "상황", 3: "장애"}
        self.csv_fp.writerow([key_map[self.type], self.time_stamp, ''.join(self.contents), result])
