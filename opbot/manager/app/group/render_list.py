# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, jsonify, current_app, request, flash)
from sqlalchemy import desc
# manager module
from app import db
from ..models import GroupInfo, GroupManagement, UserInfo

group_bp = Blueprint('group_list', __name__, url_prefix='/group')


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


@group_bp.route('/_search_group_list', methods=['POST'])
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
    cond2 = data['cond2']
    some = data['some']

    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'

    stmt = GroupInfo.query

    if cond1 == "m":
        stmt = stmt.filter(GroupInfo.owner_id == owner_id)

    if len(some) > 0 and cond2 == "g":
        stmt = stmt.filter(GroupInfo.group_name.like("%{}%".format(some.strip())))
    elif len(some) > 0 and cond2 == "o":
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


@group_bp.route('/_delete_group', methods=['POST'])
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


@group_bp.route('/_change_owner', methods=['POST'])
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
