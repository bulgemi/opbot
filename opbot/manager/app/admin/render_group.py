# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, jsonify, current_app, request, flash)
from sqlalchemy import desc
# OPBOT manager module
from app import db
from ..models import GroupInfo, GroupManagement, UserInfo

admin_bp = Blueprint('admin_group', __name__, url_prefix='/admin')


@admin_bp.route('/group', methods=('GET', 'POST'))
def render():
    """
    그룹 관리 조회 화면 로딩.
    :return:
    """
    return render_template('admin/group_manage.html')


@admin_bp.route('/_load_group_list', methods=['POST'])
def load_group_list():
    """
    Group list 조회.
    :return:
    """
    from datetime import datetime
    group_list = list()

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


@admin_bp.route('/_search_group_list', methods=['POST'])
def search_group_list():
    """
    그룹 리스트 검색 조건 처리
    :return:
    """
    from datetime import datetime
    group_list = list()

    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    cond1 = data['cond1']
    some = data['some']

    stmt = GroupInfo.query

    if len(some) > 0 and cond1 == "g":
        stmt = stmt.filter(GroupInfo.group_name.like("%{}%".format(some.strip())))
    elif len(some) > 0 and cond1 == "o":
        user_info = UserInfo.query.filter(UserInfo.user_name == some.strip()).first()
        if user_info is not None:
            stmt = stmt.filter(GroupInfo.owner_id == user_info.user_id)
    else:
        pass

    rows = stmt.order_by(desc(GroupInfo.update_time)).all()

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


@admin_bp.route('/_delete_group', methods=['POST'])
def delete_group():
    """
    그룹 삭제.
    :return:
    """
    result = dict()
    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    result['result'] = True

    try:
        stmt = GroupInfo.query.filter(GroupInfo.group_name == data['group_name'].strip())
        group_info = stmt.first()

        if group_info is not None:
            GroupManagement.query.filter(GroupManagement.group_id == group_info.group_id).delete()

        stmt.delete()
        db.session.commit()
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        flash('그룹 삭제 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
        db.session.rollback()
        result['result'] = False
    return jsonify(result=result)


@admin_bp.route('/_change_owner', methods=['POST'])
def change_owner():
    """
    소유자 변경 처리.
    :return:
    """
    result = dict()
    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    result['result'] = True

    email = data['email']
    rows = data['data']
    try:
        user_info = UserInfo.query.filter(UserInfo.email == email.strip()).first()
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        result['result'] = False
        flash('소유자 변경 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
        return jsonify(result=result)

    if user_info is not None:
        for row in rows:
            try:
                group_info = GroupInfo.query.filter(GroupInfo.group_name == row['group_name'].strip()).first()
                group_info.owner_id = user_info.user_id
                db.session.commit()
            except Exception as e:
                current_app.logger.error("!%s!" % e)
                db.session.rollback()
                result['result'] = False
    else:
        result['result'] = False
        flash('소유자 이메일이 존재하지 않습니다!', 'error')
    return jsonify(result=result)
