# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pm_svc:!pm1svc@localhost/oracle_db'

db = SQLAlchemy(app)
migrage = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class PmSvcLogMon(db.Model):
    log_num = db.Column(db.String(32), primary_key=True)
    service_id = db.Column(db.String(8), primary_key=True)
    server_os_id = db.Column(db.String(32))
    sw_instance_id = db.Column(db.String(32))
    issue_receive_date = db.Column(db.String(20))
    source_type = db.Column(db.String(16))
    msg = db.Column(db.String(4000))
    log_status_type = db.Column(db.String(1))
    splunk_domain = db.Column(db.String(16))
    splunk_item = db.Column(db.String(128))
    ev_grade = db.Column(db.String(1))
    sw_instance_type = db.Column(db.String(16))


@manager.command
def tt():
    print("tp timeout")


if __name__ == '__main__':
    manager.run()
