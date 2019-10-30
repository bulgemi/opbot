# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # charset=utf8 설정 중요!
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 500,  # bug-fix: MySQL server has gone away, my.conf: wait_timeout 보다 작아야 함.
        'pool_pre_ping': True
    }
    db.init_app(app)
    manager = Manager(app)
    # manager.add_command('db', MigrateCommand)
    logging.basicConfig(filename=Config.LOG_FILE,
                        level=Config.LOG_LEVEL,
                        format='%(levelname)s|%(asctime)s[%(filename)s:%(funcName)s(%(lineno)d) %(message)s')

    return app, manager, logging
