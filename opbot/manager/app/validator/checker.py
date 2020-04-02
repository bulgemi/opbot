# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from cerberus import Validator


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
    }

    v = Validator(schema)
    return v.validate(document), v.errors
