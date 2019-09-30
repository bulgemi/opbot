# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://opbot_appl:apbot_appl26#!@localhost/opbot_db'

db = SQLAlchemy(app)
migrage = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128))


if __name__ == '__main__':
    manager.run()
