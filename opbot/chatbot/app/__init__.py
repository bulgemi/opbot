# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os
from flask import Flask
from flask import Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from .config import Config
from .blue import add_ns

api = Api()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__)
    # charset=utf8 설정 중요!
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # RESTPlus
    api.init_app(blueprint, version='1.0', title='OPBOT APIs', description="OPBOT Rest APIs")
    add_ns(api)
    app.register_blueprint(blueprint, url_prefix='/api/1')

    manager = Manager(app)
    # manager.add_command('db', MigrateCommand)
    # logging
    if os.path.isdir(Config.LOG_DIR) is False:
        os.mkdir(Config.LOG_DIR)

    app.config['LOGGING_LEVEL'] = Config.LOG_LEVEL_CHATBOT
    app.config['LOGGING_FORMAT'] = Config.LOG_FORMAT
    app.config['LOGGING_LOCATION'] = Config.LOG_DIR
    app.config['LOGGING_FILENAME'] = Config.LOG_FILE_CHATBOT
    app.config['LOGGING_MAX_BYTES'] = 1024*100
    app.config['LOGGING_BACKUP_COUNT'] = 10
    log_full_path = "{}/{}".format(app.config['LOGGING_LOCATION'], app.config['LOGGING_FILENAME'])
    file_handler = RotatingFileHandler(log_full_path,
                                       maxBytes=app.config['LOGGING_MAX_BYTES'],
                                       backupCount=app.config['LOGGING_BACKUP_COUNT'])
    file_handler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(file_handler)
    app.logger.debug("Start Chatbot.")
    app.logger.info("Start Chatbot.")
    app.logger.warning("Start Chatbot.")
    app.logger.error("Start Chatbot.")
    app.logger.critical("Start Chatbot.")

    return app, manager
