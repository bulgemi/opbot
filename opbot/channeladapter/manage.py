# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from app import create_app, db
from app.channel_adapter_celery import make_celery

app, manager, logger = create_app()

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


@manager.command
def hello():
    print("hello")
    logger.debug("hello")


@celery.task()
def add_together(a, b):
    return a + b


@celery.task()
def task_channel_adapter():
    from app.channel_adapter import ChannelAdapter
    from app.adapter.adapter_oracle import AdapterOracle

    channel_adapter = ChannelAdapter(db, logger)
    adapter = AdapterOracle(channel_adapter)
    channel_adapter.attach(adapter)
    channel_adapter.notify_all()


if __name__ == '__main__':
    manager.run()
