# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

footer_bp = Blueprint('footer_about', __name__, url_prefix='/footer')


@footer_bp.route('/about', methods=('GET', 'POST'))
def render_about():
    return render_template('common/about.html')
