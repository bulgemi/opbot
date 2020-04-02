# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_email(to, subject, template, **kwargs):
    current_app.logger.debug("MAIL_SUBJECT_PREFIX=<%r>" % current_app.config['MAIL_SUBJECT_PREFIX'])

    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    current_app.logger.debug("msg.body=[%r]" % msg.body)
    current_app.logger.debug("msg.html=[%r]" % msg.html)

    mail.send(msg)
