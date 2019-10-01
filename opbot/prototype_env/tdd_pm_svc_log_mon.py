# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from trigger import Trigger

app = Flask(__name__)
# charset=utf8 설정 중요!
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pm_svc:!pm1svc@localhost/oracle_db?charset=utf8'

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
def trigger():
    trig = Trigger()
    data = trig.pick_event_data()

    pmsvclogmon = PmSvcLogMon()

    pmsvclogmon.log_num = data[0]
    pmsvclogmon.service_id = data[1]
    pmsvclogmon.server_os_id = data[2]
    pmsvclogmon.sw_instance_id = data[3]
    # network_id = data[4]
    # issue_date = data[5]
    pmsvclogmon.issue_receive_date = data[6]
    pmsvclogmon.source_type = data[7]
    pmsvclogmon.msg = data[8].encode('utf-8')
    pmsvclogmon.log_status_type = data[9]
    # host_name = data[10]
    # sw_instance_nm = data[11]
    # receive_id = data[12]
    # receive_date = data[13]
    # recover_id = data[14]
    # recover_date = data[15]
    # log_status_desc = data[16]
    pmsvclogmon.splunk_domain = data[17]
    pmsvclogmon.splunk_item = data[18]
    pmsvclogmon.ev_grade = data[19]
    pmsvclogmon.sw_instance_type = data[20]

    try:
        db.session.add(pmsvclogmon)
        db.session.commit()
    except IntegrityError as e:
        print("!%r!" % str(e.orig))
        db.session.rollback()


@manager.command
def clear():
    db.session.query(PmSvcLogMon).delete()
    db.session.commit()


if __name__ == '__main__':
    manager.run()
