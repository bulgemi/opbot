# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import Flask, request

app = Flask('SlackReceiver')


@app.route('/slack/message', methods=['GET', 'POST'])
def incoming_slack_message():
    req = request.get_json()
    # .. do something with the req ..
    print("------------------>", req)
    return 'action successful'


@app.route('/slack/options', methods=['GET', 'POST', 'OPTIONS'])
def incoming_slack_options():
    # .. idk ..
    print("==================>")
    return 'ok'


if __name__ == '__main__':
    app.run('192.168.43.157', 8088, debug=False)
