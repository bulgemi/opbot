# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
from app import create_app, db
from app.bot import ChatBot
from app.chatbot_celery import make_celery

app, manager = create_app()

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6389',
    CELERY_RESULT_BACKEND='redis://localhost:6389'
)
celery = make_celery(app)

with app.app_context():
    app.bot = ChatBot(db)


@celery.task()
def task_execute(task_id, out_channel_id):
    """
    Task Executor 에게 REST API 요청(Async Task Queue)
    :param task_id:
    :param out_channel_id:
    :return:
    """
    return current_app.bot.task_execute(task_id, out_channel_id)


@celery.task()
def put_collector(event_uid, task_id, exec_type):
    """
    Collector 에 사용자 이벤트 전송.(Async Task Queue)
    :param event_uid:
    :param task_id:
    :param exec_type:
    :return:
    """
    return current_app.bot.put_collect(event_uid, task_id, exec_type)


if __name__ == '__main__':
    manager.run()
