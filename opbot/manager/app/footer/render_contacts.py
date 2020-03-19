# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint)
# OPBOT manager module

footer_bp = Blueprint('footer_contacts', __name__, url_prefix='/footer')


@footer_bp.route('/contacts', methods=('GET', 'POST'))
def render_sitemap():
    return render_template('common/contacts.html')
