# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
from cerberus import Validator


def check_forbidden_instruction(script):
    """
    script 내용에 금칙어가 존재하는 확인
    :param script:
    :return:
    """
    f_list = current_app.config['FORBIDDEN_INSTRUCTION']
    msg = ""
    i = 0

    for f in f_list:
        if script.find(f) != -1:
            t = '{}'.format(f)
            if i != 0:
                msg += ", "
            msg += t
            i += 1

    return True if i == 0 else False, "[{}]은 금칙어 입니다!".format(msg)


def check(document):
    schema = {
        'name': {'type': 'string',
                 'empty': False,
                 'minlength': 2,
                 'maxlength': 32},
        'email': {'type': 'string',
                  'empty': False,
                  'minlength': 5,
                  'maxlength': 150,
                  'regex': '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'password': {'type': 'string',
                     'empty': False,
                     'minlength': 8,
                     'maxlength': 15,
                     'regex': '^.*(?=^.{8,15}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$'},
        'task': {'type': 'string',
                 'empty': False,
                 'minlength': 5,
                 'maxlength': 100},
        'task_type': {'type': 'string',
                      'empty': False,
                      'minlength': 1,
                      'maxlength': 1,
                      'regex': '0|1|2|3|4'},
        'action_type': {'type': 'string',
                        'empty': False,
                        'minlength': 1,
                        'maxlength': 1,
                        'regex': 'A|S'},
        'task_cause': {'type': 'string',
                       'empty': False,
                       'minlength': 10,
                       'maxlength': 100},
    }

    v = Validator(schema)
    return v.validate(document), v.errors
