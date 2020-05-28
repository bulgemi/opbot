# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pandas as pd


class DataPreprocessor(object):
    def __init__(self, xlsx):
        self.data = pd.read_excel(xlsx)
        self.type = None
        self.key_value = ""
        self.measure = False
        self.s_close = False
        self.contents = []
        self.key_map = {"통합품질감시": 0, "장애의심": 1, "상황": 2, "장애": 3}

    def __del__(self):
        pass

    def read_xls(self):
        pass

    def get_type(self, row):
        return row['장애구분']

    def get_send_message(self, row):
        return row['발송메시지']

    def parse_row(self):
        pass

    def find_key_word(self, key_word):
        pass

    def data_filter(self, row):
        import re
        f_row = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》{}]', '', row)
        return f_row
