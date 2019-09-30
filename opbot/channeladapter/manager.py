# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import Flask, request
from flask_script import Manager
from flask_restplus import Api, Resource
from .channel_adapter import ChannelAdapter
from .adapter_oracle import AdapterOracle


def create_app(config=None):
    app = Flask(__name__)
    api = Api()
    api.init_app(app)
    return app, api


app, api = create_app()
manager = Manager(app)


@manager.command
def hello():
    print("hello")


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {}


@api.route('/<string:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


if __name__ == '__main__':
    manager.run()
