# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pandas as pd
import re
import os
import csv


class StopWord(object):
    def __init__(self, csv_file):
        """
        불용어 초기화.
        :param csv_file:
        """
        self.data = pd.read_csv(csv_file)
        self.stat_map = {"통합품질감시": 0, "장애의심": 0, "상황": 0, "장애": 0}
        self.stop_words = [
            r'\D{2,4}?(선임|수석|매니저|메니저)',
            r'\d{2,3}[:\.\s]*\d{2,2}(?!\d)',
            r'\(\d{3}\)\s*\d{4}[-\.\s]??\d{4}',
            r'\d{1,3}[,\.]\d{1,3}',
            r'\d{1,4}[년]\d{1,2}[월]\d{1,2}[일]',
            r'\d{1,4}[년]\s\d{1,2}[월]\s\d{1,2}[일]',
            r'\d{1,2}[월]\s\d{1,2}[일]',
            r'\d{1,2}[월]\d{1,2}[일]',
            r'IT종합상황실 상황관리자',
            r'Ontune',
            r'AnyCatcher',
        ]
        self.fp = open(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/Rims_stopword.csv", 'w')
        self.len_list = list()

    def __del__(self):
        self.fp.close()

    def remove_special_characters(self, row):
        """
        특수문자 제거.
        :param row:
        :return:
        """
        f_row = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》{}_●]', '', row)
        return f_row

    def do_stopword(self, row):
        """
        불용어 처리
        :param row:
        :return:
        """
        for r in self.stop_words:
            row = re.sub(r, '', row)
        return row

    def data_info(self):
        print(self.data.shape)
        print("%r" % self.stat_map)
        print("최장 문자 길자=%d, 평균 문자 길이=%d" % (max(self.len_list), sum(self.len_list)/len(self.len_list)))

    def read_column(self):
        csv_fp = csv.writer(self.fp, delimiter=',')

        for i, r in self.data.iterrows():
            self.stat_map[r[0]] += 1
            # print("%r=%r" % (i, r[2]))
            row = self.do_stopword(r[2])
            rsc = self.remove_special_characters(row)
            self.len_list.append(len(rsc))
            # print("%r" % rsc)
            # print("%r=%r" % (i, r[3]))

            if pd.isnull(r[3]):
                csv_fp.writerow([r[0], rsc.lower(), r[3]])
            else:
                result_row = self.do_stopword(r[3])
                result_rsc = self.remove_special_characters(result_row)
                csv_fp.writerow([r[0], rsc.lower(), result_rsc.lower()])
                # print("%r" % r[2])
                # print("%r" % rsc)


if __name__ == '__main__':
    stopword = StopWord("data/Rims_result.csv")
    stopword.read_column()
    stopword.data_info()
