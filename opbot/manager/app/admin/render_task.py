# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, request, jsonify, current_app, flash)
from sqlalchemy import desc
# OPBOT manager module
from app import db
from ..models import TaskInfo, UserInfo

admin_bp = Blueprint('admin_task', __name__, url_prefix='/admin')
task_type_map = {
    0: "OPMATE",
    1: "K8s",
    2: "Command",
    3: "Shell Script",
    4: "Ansible"
}
action_type_map = {
    'A': "분석",
    'S': "조치"
}
status_map = {
    0: "비정상",
    1: "정상",
    2: "잠김",
    3: "임시"
}


@admin_bp.route('/task', methods=('GET', 'POST'))
def render():
    """
    태스크 관리 화면 로딩.
    :return:
    """
    return render_template('admin/task_manage.html')


@admin_bp.route('/_load_task_list', methods=['POST'])
def load_task_list():
    """
    Task list 조회.
    :return:
    """
    from datetime import datetime
    task_list = list()
    global task_type_map
    global action_type_map
    global status_map

    rows = TaskInfo.query.order_by(desc(TaskInfo.update_time)).all()

    for row in rows:
        audit_info = UserInfo.query.filter_by(user_id=row.audit_id).first()
        create_obj = datetime.strptime(row.create_time, "%Y%m%d%H%M%S")
        update_obj = datetime.strptime(row.update_time, "%Y%m%d%H%M%S")

        if audit_info is None:
            audit_val = "N/A"
        else:
            audit_val = "{0}({1})".format(audit_info.user_name, audit_info.email)

        task_list.append({
            "task_name": row.task_name,
            "task_type": task_type_map[row.task_type],
            "action_type": action_type_map[row.action_type],
            "create_time": create_obj.strftime("%Y/%m/%d"),
            "update_time": update_obj.strftime("%Y/%m/%d"),
            "audit": audit_val,
            "status": status_map[row.status_code]
        })

    return jsonify(result=task_list)


@admin_bp.route('/_search_task_list', methods=['POST'])
def search_task_list():
    from datetime import datetime
    task_list = list()
    global task_type_map
    global action_type_map
    global status_map
    inv_task_type_map = {v: k for k, v in task_type_map.items()}
    inv_action_type_map = {v: k for k, v in action_type_map.items()}
    inv_status_map = {v: k for k, v in status_map.items()}

    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'

    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    cond1 = data['cond1']
    some = data['some']

    stmt = TaskInfo.query

    if len(some) > 0 and cond1 == "n":
        stmt = stmt.filter(TaskInfo.task_name.like("%{}%".format(some.strip())))
    elif len(some) > 0 and cond1 == "t":
        cond = inv_task_type_map[some.strip()]

        if cond is not None:
            stmt = stmt.filter(TaskInfo.task_type == cond)
    elif len(some) > 0 and cond1 == "a":
        cond = inv_action_type_map[some.strip()]

        if cond is not None:
            stmt = stmt.filter(TaskInfo.action_type == cond)
    elif len(some) > 0 and cond1 == "e":
        user_info = UserInfo.query.filter(UserInfo.email == some.strip()).first()
        if user_info is not None:
            stmt = stmt.filter(TaskInfo.owner_id == user_info.user_id)
    elif len(some) > 0 and cond1 == "s":
        cond = inv_status_map[some.strip()]

        if cond is not None:
            stmt = stmt.filter(TaskInfo.status_code == cond)
    else:
        pass

    rows = stmt.order_by(desc(TaskInfo.update_time)).all()

    for row in rows:
        audit_info = UserInfo.query.filter_by(user_id=row.audit_id).first()
        create_obj = datetime.strptime(row.create_time, "%Y%m%d%H%M%S")
        update_obj = datetime.strptime(row.update_time, "%Y%m%d%H%M%S")

        if audit_info is None:
            audit_val = "N/A"
        else:
            audit_val = "{0}({1})".format(audit_info.user_name, audit_info.email)

        task_list.append({
            "task_name": row.task_name,
            "task_type": task_type_map[row.task_type],
            "action_type": action_type_map[row.action_type],
            "create_time": create_obj.strftime("%Y/%m/%d"),
            "update_time": update_obj.strftime("%Y/%m/%d"),
            "audit": audit_val,
            "status": status_map[row.status_code]
        })
    current_app.logger.debug("task_list=%r" % task_list)
    return jsonify(result=task_list)


@admin_bp.route('/_delete_task', methods=['POST'])
def delete_task_list():
    result = dict()
    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    result['result'] = True

    try:
        TaskInfo.query.filter(TaskInfo.task_name == data['task_name'].strip()).delete()
        db.session.commit()
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        flash('태스크 삭제 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
        db.session.rollback()
        result['result'] = False
    return jsonify(result=result)


@admin_bp.route('/_lock_task', methods=['POST'])
def lock_task():
    """
    태스트 잠금/해제
    :return:
    """
    result = dict()
    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    result['result'] = True

    rows = data['data']

    for row in rows:
        try:
            task_info = TaskInfo.query.filter(TaskInfo.task_name == row['task_name'].strip()).first()

            if task_info.status_code == 2:
                task_info.status_code = 1
            else:
                task_info.status_code = 2
            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            result['result'] = False

    return jsonify(result=result)
