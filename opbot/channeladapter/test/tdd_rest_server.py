# _*_ coding: utf-8 _*_
from flask import Flask, request
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


@api.route('/notify')
class HelloWorld(Resource):
    def post(self):
        print(request.form.get('CHANNEL_ID'))
        print(request.form.get('EVENT_MSG'))
        print(request.form.get('EVENT_UID'))
        return request.get_json()
        # return {'hello': 'world'}


if __name__ == '__main__':
    app.run(port=5555, debug=True)
