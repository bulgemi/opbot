# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
sys.path.append(os.getenv('OPBOT_HOME'))


def test_step1():
    """
    step1 기능 점검
    :return:
    """
    from datapreprocessor.step1 import Step1

    dp = Step1(os.getenv('OPBOT_HOME') + "/datapreprocessor/data/Rims_history.xlsx")
    assert dp.read_xls() is True
