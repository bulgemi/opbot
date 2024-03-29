# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os
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
    # logging
    if os.path.isdir(Config.LOG_DIR) is False:
        os.mkdir(Config.LOG_DIR)

    app.config['LOGGING_LEVEL'] = Config.LOG_LEVEL
    app.config['LOGGING_FORMAT'] = Config.LOG_FORMAT
    app.config['LOGGING_LOCATION'] = Config.LOG_DIR
    app.config['LOGGING_FILENAME'] = Config.LOG_FILE
    app.config['LOGGING_MAX_BYTES'] = 1024 * 100
    app.config['LOGGING_BACKUP_COUNT'] = 10
    log_full_path = "{}/{}".format(app.config['LOGGING_LOCATION'], app.config['LOGGING_FILENAME'])
    file_handler = RotatingFileHandler(log_full_path,
                                       maxBytes=app.config['LOGGING_MAX_BYTES'],
                                       backupCount=app.config['LOGGING_BACKUP_COUNT'])
    file_handler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(file_handler)

    return app, manager, logging
