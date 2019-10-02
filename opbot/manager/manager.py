# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from app import create_app
from app import models

app, manager = create_app()


@manager.command
def hello():
    print("hello")


if __name__ == '__main__':
    manager.run()
