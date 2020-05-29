# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import shutil
import pandas as pd
from .datapreprocessor import DataPreprocessor


class Step1(DataPreprocessor):
    def do_type0(self, f_msg, o_msg):
        if f_msg.find("●서버:") != -1:
            l_tmp = f_msg.split("●서버:")
            self.key_value = self.data_filter(l_tmp[1])

        if f_msg.find("●메시지:") != -1:
            l_tmp = f_msg.split("●메시지:")
            self.key_value += self.data_filter(l_tmp[1])

        if f_msg.find("●조치") != -1:
            self.measure = True

        self.contents.append(o_msg)

        if self.measure is True:
            if f_msg.find("상황종료") != -1 or f_msg.find("장애종료") != -1:
                self.s_close = True
                # print("=" * 50)
                # print("type: %s" % self.type)
                # print("key: %s" % self.key_value)
                # print("contents: <%r>" % self.contents)
                self.save_data()
        return

    def do_type2(self, f_msg, o_msg):
        if f_msg.find("●내용:") != -1:
            l_tmp = f_msg.split("●내용:")
            self.key_value = self.data_filter(l_tmp[1])

        if f_msg.find("●조치") != -1:
            self.measure = True

        self.contents.append(o_msg)

        if self.measure is True:
            if f_msg.find("상황종료") != -1 or f_msg.find("장애종료") != -1:
                self.s_close = True
                # print("=" * 50)
                # print("type: %s" % self.type)
                # print("key: %s" % self.key_value)
                # print("contents: <%r>" % self.contents)
                self.save_data()
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

        if f_msg.find("●조치") != -1:
            self.measure = True

        self.contents.append(o_msg)

        if self.measure is True:
            if f_msg.find("상황종료") != -1 or f_msg.find("장애종료") != -1:
                self.s_close = True
                # print("=" * 50)
                # print("type: %s" % self.type)
                # print("key: %s" % self.key_value)
                # print("contents: <%r>" % self.contents)
                self.save_data()
        return

    def read_xls(self):
        for i, r in self.data.iterrows():
            if pd.isnull(self.get_type(r)):
                pass
            else:
                self.type = self.key_map[self.get_type(r)]
                self.measure = False
                self.s_close = False
                self.contents.clear()

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

    def clear_data(self):
        import os

        shutil.rmtree(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/preprocess_data/", ignore_errors=True)
        os.makedirs(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/preprocess_data/0", exist_ok=True)
        os.makedirs(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/preprocess_data/1", exist_ok=True)
        os.makedirs(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/preprocess_data/2", exist_ok=True)
        os.makedirs(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/preprocess_data/3", exist_ok=True)

    def save_data(self):
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
        full_path = os.getenv('OPBOT_HOME') + save_dir + tmp
        os.makedirs(full_path, exist_ok=True)

        with open(full_path+"/r.txt", 'w') as f:
            f.write(''.join(self.contents))
