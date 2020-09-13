# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, request, jsonify, current_app, flash)
from sqlalchemy import desc
# OPBOT manager module
from app import db
from ..models import UserInfo

admin_bp = Blueprint('admin_user', __name__, url_prefix='/admin')


@admin_bp.route('/user', methods=('GET', 'POST'))
def render():
    """
    사용자 관리 화면 로딩.
    :return:
    """
    return render_template('admin/user_manage.html')


@admin_bp.route('/_load_user_list', methods=['POST'])
def load_user_list():
    """
    User list 조회.
    :return:
    """
    from datetime import datetime
    user_list = list()

    rows = UserInfo.query.order_by(desc(UserInfo.update_time)).all()

    for row in rows:
        create_obj = datetime.strptime(row.create_time, "%Y%m%d%H%M%S")
        update_obj = datetime.strptime(row.update_time, "%Y%m%d%H%M%S")

        user_list.append({
            "user_id": row.user_id,
            "user_name": row.user_name,
            "email": row.email,
            "slack_id": row.slack_id,
            "create_time": create_obj.strftime("%Y/%m/%d"),
            "update_time": update_obj.strftime("%Y/%m/%d"),
            "status": row.status_code,
            "role": row.role_code
        })

    return jsonify(result=user_list)


@admin_bp.route('/_search_user_list', methods=['POST'])
def search_user_list():
    """
    사용자 관리 검색 처리.
    :return:
    """
    from datetime import datetime
    user_list = list()

    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    cond1 = data['cond1']
    some = data['some']

    stmt = UserInfo.query

    if len(some) > 0 and cond1 == "u":
        stmt = stmt.filter(UserInfo.user_name.like("%{}%".format(some.strip())))
    elif len(some) > 0 and cond1 == "e":
        stmt = stmt.filter(UserInfo.email.like("%{}%".format(some.strip())))
    elif len(some) > 0 and cond1 == "s":
        status_code_map = {
            "잠금": 0,
            "활성": 1
        }

        if some.strip() not in status_code_map:
            return jsonify(result=user_list)

        stmt = UserInfo.query.filter(UserInfo.status_code == status_code_map[some.strip()])
    elif len(some) > 0 and cond1 == "r":
        role_code_map = {
            "일반사용자": 2,
            "그룹관리자": 1,
            "관리자": 0
        }

        some = some.replace(" ", "")
        if some not in role_code_map:
            return jsonify(result=user_list)

        stmt = UserInfo.query.filter(UserInfo.role_code == role_code_map[some])
    else:
        pass

    rows = stmt.order_by(desc(UserInfo.update_time)).all()

    for row in rows:
        create_obj = datetime.strptime(row.create_time, "%Y%m%d%H%M%S")
        update_obj = datetime.strptime(row.update_time, "%Y%m%d%H%M%S")

        user_list.append({
            "user_id": row.user_id,
            "user_name": row.user_name,
            "email": row.email,
            "slack_id": row.slack_id,
            "create_time": create_obj.strftime("%Y/%m/%d"),
            "update_time": update_obj.strftime("%Y/%m/%d"),
            "status": row.status_code,
            "role": row.role_code
        })

    current_app.logger.debug("task_list=%r" % user_list)
    return jsonify(result=user_list)


@admin_bp.route('/_add_user', methods=['POST'])
def add_user_list():
    """
    사용자 추가.
    :return:
    """
    from datetime import datetime
    from uuid import uuid1
    from ..validator.checker import check
    from ..common.set_resp_msg import set_detail_result

    moss = current_app.config['MOSS']
    result = dict()
    result['result'] = True

    data = request.get_json()
    current_app.logger.debug("data=%r" % data)

    user_name = data['user_name']
    email = data['email']
    slack_id = data['slack_id']
    status_code = data['status']
    role_code = data['role']

    # 1.형식 검사: 사용자명.
    c, e = check({'name': user_name})
    r, d = set_detail_result(c, '잘봇된 형식입니다! (최소: 2자, 최대 32자)')
    result['result'] = r if r is False else result['result']

    if result['result'] is False:
        flash("잘봇된 사용자명 형식입니다! (최소: 2자, 최대 32자)", 'warning')
        return result

    # 1.형식 검사: 이메일.
    c, e = check({'email': email})
    r, d = set_detail_result(c, '잘못된 형식입니다! (최소 5자, 최대 150자)')
    result['result'] = r if r is False else result['result']

    # 2.DB 존재 여부 확인.
    if result['result'] is True:
        user = UserInfo.query.filter_by(email=email).first()

        if user is not None:
            r, d = set_detail_result(False, '존재하는 이메일입니다! (최소 5자, 최대 150자)')
            result['result'] = r if r is False else result['result']

    if result['result'] is False:
        flash("잘못된 형식 이거나 존재하는 이메일입니다! (최소 5자, 최대 150자)", 'warning')
        return result

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    new_user_id = 'u_' + str(uuid1())

    try:
        new_user = UserInfo(
            user_id=new_user_id,
            user_name=user_name,
            email=email,
            passwd=moss.enc('1234567890'),
            status_code=status_code,
            role_code=role_code,
            slack_id=slack_id if slack_id is not None else "",
            create_time=current_time,
            update_time=current_time
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        flash("사용자 추가에 실패하였습니다! 관리자에 문의하세요.", 'error')
        db.session.rollback()
        raise e
    flash("사용자 추가 완료하였습니다.", 'success')
    return jsonify(result=result)


@admin_bp.route('/_update_user', methods=['POST'])
def update_user_list():
    """
    사용자 정보 수정.
    :return:
    """
    from datetime import datetime

    result = dict()
    result['result'] = True

    data = request.get_json()
    current_app.logger.debug("data=%r" % data)

    user_id = data['user_id']
    user_name = data['user_name']
    email = data['email']
    slack_id = data['slack_id']
    status_code = data['status']
    role_code = data['role']

    try:
        user = UserInfo.query.filter_by(user_id=user_id).first()

        if user is None:
            flash("사용자 정보가 없습니다!", 'warning')
            result['result'] = False
        else:
            current_time = datetime.now().strftime('%Y%m%d%H%M%S')
            user.user_name = user_name
            user.email = email
            user.slack_id = slack_id
            user.status_code = status_code
            user.role_code = role_code
            user.update_time = current_time
            db.session.commit()
    except Exception as e:
        result['result'] = False
        current_app.logger.error("!%s!" % e)
        flash("사용자 수정에 실패하였습니다! 관리자에 문의하세요.", 'error')
        db.session.rollback()
    flash("사용자 수정을 완료하였습니다.", 'success')
    return jsonify(result=result)


@admin_bp.route('/_delete_user', methods=['POST'])
def delete_user_list():
    """
    사용자 삭제.
    :return:
    """
    result = dict()
    result['result'] = True

    data = request.get_json()
    current_app.logger.debug("data=%r" % data)

    user_id = data['user_id']

    try:
        UserInfo.query.filter_by(user_id=user_id).delete()
        db.session.commit()
    except Exception as e:
        result['result'] = False
        current_app.logger.error("!%s!" % e)
        flash("사용자 삭제에 실패하였습니다! 관리자에 문의하세요.", 'error')
        db.session.rollback()
    flash("사용자 삭제에 완료하였습니다.", 'success')
    return jsonify(result=result)
