# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, jsonify, current_app)
from sqlalchemy import desc
# manager module
from app import db
from ..models import GroupInfo, UserInfo

group_bp = Blueprint('group_list', __name__, url_prefix='/group')
status_map = {
    0: "비정상",
    1: "정상",
    2: "잠김",
    3: "임시"
}


@group_bp.route('/list', methods=('GET', 'POST'))
def render():
    """
    그룹 조회 화면 로딩.
    :return:
    """
    return render_template('group/group_list.html')


@group_bp.route('/_load_group_list', methods=['POST'])
def load_group_list():
    """
    Group list 조회.
    :return:
    """
    from datetime import datetime
    group_list = list()
    global status_map

    rows = GroupInfo.query.order_by(desc(GroupInfo.update_time)).all()

    for row in rows:
        current_app.logger.debug("row=%r" % row.group_name)
        user_info = UserInfo.query.filter_by(user_id=row.owner_id).first()
        create_obj = datetime.strptime(row.create_time, "%Y%m%d%H%M%S")
        update_obj = datetime.strptime(row.update_time, "%Y%m%d%H%M%S")
        audit_info = UserInfo.query.filter_by(user_id=row.audit_id).first()
        if user_info is None:
            user_val = "N/A"
        else:
            user_val = "{0}({1})".format(user_info.user_name, user_info.email)

        if audit_info is None:
            audit_val = "N/A"
        else:
            audit_val = "{0}({1})".format(audit_info.user_name, audit_info.email)
        group_list.append({
            "group_name": row.group_name,
            "owner": user_val,
            "create_time": create_obj.strftime("%Y/%m/%d"),
            "update_time": update_obj.strftime("%Y/%m/%d"),
            "audit": audit_val,
        })

    return jsonify(result=group_list)
