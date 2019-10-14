# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from app import create_app, db

app, manager = create_app()

if __name__ == '__main__':
    manager.run()
