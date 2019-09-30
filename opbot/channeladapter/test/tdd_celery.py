# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def add(x, y):
    return x + y
