# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from .step1 import Step1

if __name__ == "__main__":
    dp = Step1("datapreprocessor/data/Rims_history.xlsx")
    dp.clear_data()
    dp.read_xls()
