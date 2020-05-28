# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from .step1 import Step1
from .step2 import Step2

if __name__ == "__main__":
    s1 = Step1("datapreprocessor/data/Rims_history.xlsx")
    s1.clear_data()
    s1.read_xls()
    s2 = Step2("datapreprocessor/data/Rims_history.xlsx")
    s2.create_csv()
    s2.read_xls()
    s2.close_csv()
