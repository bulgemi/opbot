# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

login_bp = Blueprint('login_new', __name__)


@login_bp.route('/new', methods=('GET', 'POST'))
def render():
    return render_template('login/user_new.html')
