# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from datetime import datetime
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
    r = analyzer.origin_dataset_generate()  # 학습 원천 데이터 생성.
    # 전처리 가공된 학습 데이터 생성.
    if r is True:
        now = datetime.now()
        now_date = now.strftime('%Y%m%d')
        # 1.Grouping
        r = analyzer.dataset_grouping(now_date)
        # 2.Classfy
        if r is True:
            r = analyzer.dataset_classfy(now_date)
        # 3.adding
        r = analyzer.dataset_adding(now_date)
    return r


if __name__ == '__main__':
    manager.run()
