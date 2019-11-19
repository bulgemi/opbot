# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
from app import create_app, db
from app.recommend import Recommender

app, manager = create_app()

with app.app_context():
    app.recommender = Recommender(db)


if __name__ == '__main__':
    manager.run()
