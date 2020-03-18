# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

admin_bp = Blueprint('admin_task', __name__, url_prefix='/admin')


@admin_bp.route('/task', methods=('GET', 'POST'))
def render():
    return render_template('admin/task_manage.html')
