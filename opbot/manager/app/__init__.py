# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    # charset=utf8 설정 중요!
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    mail.init_app(app)

    # register blueprint
    from .bp import register_bp
    register_bp(app)

    # logging
    if os.path.isdir(Config.LOG_DIR_MANAGER) is False:
        os.mkdir(Config.LOG_DIR_MANAGER)

    app.config['LOGGING_LEVEL'] = Config.LOG_LEVEL_MANAGER
    app.config['LOGGING_FORMAT'] = Config.LOG_FORMAT_MANAGER
    app.config['LOGGING_LOCATION'] = Config.LOG_DIR_MANAGER
    app.config['LOGGING_FILENAME'] = Config.LOG_FILE_MANAGER
    app.config['LOGGING_MAX_BYTES'] = 1024*100
    app.config['LOGGING_BACKUP_COUNT'] = 10
    log_full_path = "{}/{}".format(app.config['LOGGING_LOCATION'], app.config['LOGGING_FILENAME'])
    file_handler = RotatingFileHandler(log_full_path,
                                       maxBytes=app.config['LOGGING_MAX_BYTES'],
                                       backupCount=app.config['LOGGING_BACKUP_COUNT'])
    file_handler.setFormatter(Formatter(app.config['LOGGING_FORMAT']))
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(file_handler)

    # RSA
    from .fishbowl.moss import Moss
    from .fishbowl.scraper import Scraper
    moss = Moss()
    moss.load_public_key(Config.PUBLIC_KEY)
    scraper = Scraper()
    scraper.load_private_key(Config.PRIVATE_KEY)

    app.config['MOSS'] = moss
    app.config['SCRAPER'] = scraper

    return app, manager
