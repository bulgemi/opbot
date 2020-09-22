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
def task_execute(task_id, out_channel_id, task_name, task_type, target_list, playbook_contents, exe_type=0):
    """
    Task Executor 에게 REST API 요청(Async Task Queue)
    :param task_id:
    :param out_channel_id:
    :param task_name:
    :param task_type:
    :param target_list:
    :param playbook_contents:
    :param exe_type:
    :return:
    """
    return current_app.bot.task_execute(task_id, out_channel_id, task_name, task_type,
                                        target_list, playbook_contents, exe_type)


@celery.task()
def cpu_execute(out_channel_id, node_list):
    """
    CPU Usage 생성 비동기 수행.(Async Task Queue)
    :param out_channel_id:
    :param node_list:
    :return:
    """
    return current_app.bot.cpu_execute(out_channel_id, node_list)


@celery.task()
def mem_execute(out_channel_id, node_list):
    """
    Memory Usage 생성 비동기 수행.(Async Task Queue)
    :param out_channel_id:
    :param node_list:
    :return:
    """
    return current_app.bot.mem_execute(out_channel_id, node_list)


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
