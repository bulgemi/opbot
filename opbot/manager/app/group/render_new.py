# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, request, jsonify, current_app, flash)
# manager module
from ..models import GroupInfo
from ..validator.checker import check
from ..common.set_resp_msg import set_detail_result

group_bp = Blueprint('group_new', __name__, url_prefix='/group')


@group_bp.route('/new', methods=('GET', 'POST'))
def render():
    return render_template('group/group_new.html')


@group_bp.route('/_check_group_name', methods=['POST'])
def check_group_name():
    """
    그룹이름 점검.
    1.형식 검사.
    2.중복 검사.
    :return:
    """
    result = dict()
    detail = dict()

    result['result'] = True
    group_name = request.form['group_name']
    current_app.logger.debug("group_name=[%s]" % group_name)

    # 1.형식 검사.
    c, e = check({'group': group_name})
    r, d = set_detail_result(c, '잘못된 형식입니다! (최소: 5자, 최대 100자)')
    result['result'] = r if r is False else result['result']
    detail['group_name'] = d

    # 2.중복 검사.
    if result['result'] is True:
        try:
            if GroupInfo.query.filter_by(group_id=group_name).first() is not None:
                r, d = set_detail_result(False, '존재하는 그룹 이름입니다! (최소 5자, 최대 100자)')
                result['result'] = r if r is False else result['result']
                detail['group_name'] = d
            else:
                r, d = set_detail_result(True, 'OK')
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            flash('그룹 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
            result['result'] = False
    result['detail'] = detail
    return jsonify(result=result)
