# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from app import create_app, db
from app.analysis_celery import make_celery

app, manager, logger = create_app()

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6399',
    CELERY_RESULT_BACKEND='redis://localhost:6399'
)
celery = make_celery(app)


@celery.task()
def task_channel_adapter():
    from app.analysis import Analyzer

    analyzer = Analyzer(db, logger)


if __name__ == '__main__':
    manager.run()
