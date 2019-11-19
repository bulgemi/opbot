# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from .event_controller import event_a as event_ns


def add_ns(api):
    api.add_namespace(event_ns)
