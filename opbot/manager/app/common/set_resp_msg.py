# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'


def set_detail_result(c, msg):
    """
    checker 결과를 기반으로 상세 결과 메시지 생성.
    :param c:
    :param msg:
    :return:
    """
    detail = dict()

    if c is False:
        detail['class'] = 'validation error',
        detail['tip'] = [msg]
    else:
        detail['tip'] = ['OK']
    return c, detail
