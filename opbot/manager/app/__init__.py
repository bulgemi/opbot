# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # charset=utf8 설정 중요!
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    # register blueprint
    from .bp import register_bp
    register_bp(app)

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
