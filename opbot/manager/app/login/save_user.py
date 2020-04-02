# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
# OPBOT manager module
from app import db
from ..models import UserInfo


class NewUser(object):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.uid = None

    def create(self):
        """
        사용자 생성처리.
        :return:
        """
        from uuid import uuid1
        from datetime import datetime

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        moss = current_app.config['MOSS']
        self.uid = 'u_' + str(uuid1())
        try:
            newbie = UserInfo(user_id=self.uid,
                              user_name=self.name,
                              email=self.email,
                              passwd=moss.enc(self.password),
                              status_code=0,
                              role_code=2,
                              slack_id='',
                              create_time=current_time,
                              update_time=current_time)
            db.session.add(newbie)
            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            raise e

    def send_mail(self):
        """
        사용자 email로 계정 활성화 링크 전송.
        :return:
        """
        from flask import url_for
        from ..email import send_email

        user = {'name': self.name,
                'url': '{}'.format(url_for('login_new.confirm', uid=self.uid, _external=True))}

        try:
            send_email(self.email, 'Confirm Your Account', 'email/confirm', user=user)
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            raise e
