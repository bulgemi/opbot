# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

login_bp = Blueprint('login', __name__)


@login_bp.route('/', methods=('GET', 'POST'))
def render():
    return render_template('login/login.html')
