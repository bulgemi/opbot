# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

task_bp = Blueprint('task_list', __name__, url_prefix='/task')


@task_bp.route('/list', methods=('GET', 'POST'))
def render():
    return render_template('task/task_list.html')
