# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

group_bp = Blueprint('group_list', __name__, url_prefix='/group')


@group_bp.route('/list', methods=('GET', 'POST'))
def render():
    return render_template('group/group_list.html')
