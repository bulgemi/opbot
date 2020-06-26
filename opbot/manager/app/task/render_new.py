# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, request, jsonify, current_app, flash, redirect, url_for)
# OPBOT manager module
from ..models import TaskInfo, TaskPlaybook, TargetList
from .save_task import NewTask
from ..validator.checker import check, check_forbidden_instruction
from ..common.set_resp_msg import set_detail_result

task_bp = Blueprint('task_new', __name__, url_prefix='/task')
masking = "******"


@task_bp.route('/new', methods=('GET', 'POST'))
def render():
    return render_template('task/task_new.html')


@task_bp.route('/new/<uid>', methods=['GET'])
def edit(uid):
    """
    태스크 정의 수정.
    :param uid:
    :return:
    """
    current_app.logger.debug("uid=<%r>" % uid)

    # 복호화
    sc = current_app.config['SCRAPER']
    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'
    ti = TaskInfo.query.filter_by(task_id=uid).first()
    tp = TaskPlaybook.query.filter_by(task_id=uid).first()

    current_app.logger.debug("ti=<%r, %r, %r, %r>"
                             % (ti.task_name, ti.task_type, ti.action_type, ti.status_code))
    contents = sc.dec(tp.contents) if tp.contents is not None else ''
    current_app.logger.debug("tp=<(%r)%r, %r>"
                             % (type(contents), contents, tp.cause))

    form = dict()
    form['uid'] = uid
    form['task_name'] = ti.task_name
    form['task_type'] = ti.task_type
    form['action_type'] = ti.action_type
    form['status_code'] = ti.status_code
    form['contents'] = contents
    form['cause'] = tp.cause
    return render_template('task/task_new.html', form=form)


@task_bp.route('/_check_task_name', methods=['POST'])
def check_task_name():
    """
    태스크 명 처리
    1.형식 검사.
    2.임시 저장, uuid 발급.
    :return:
    """
    result = dict()
    rdata = dict()
    detail = dict()

    result['result'] = True
    task_uid = request.form['task_uid']
    name = request.form['name']
    task_type = request.form['task_type']
    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.06. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'
    action_type = request.form['action_type']
    # 1.형식 검사.
    current_app.logger.debug("task_uid=[%s], task_name=[%s], task_type=[%s], action_type=[%s]"
                             % (task_uid, name, task_type, action_type))
    # task name
    c, e = check({'task': name})
    r, d = set_detail_result(c, '잘못된 형식입니다! (최소: 5자, 최대 100자)')

    result['result'] = r if r is False else result['result']
    detail['task_name'] = d
    # task type
    c, e = check({'task_type': task_type})
    r, d = set_detail_result(c, '잘못된 형식입니다!')

    result['result'] = r if r is False else result['result']
    detail['task_type'] = d
    # action type
    c, e = check({'action_type': action_type})
    r, d = set_detail_result(c, '잘못된 형식입니다!')

    result['result'] = r if r is False else result['result']
    detail['action_type'] = d

    # 2.DB 존재 여부 확인.
    if result['result'] is True:
        try:
            new_task = NewTask()
            # Check Task Name
            if TaskInfo.query.filter_by(task_name=name).first() is not None:
                r, d = set_detail_result(False, '존재하는 태스크 이름입니다! (최소 5자, 최대 150자)')
                result['result'] = r if r is False else result['result']
                detail['task_name'] = d
            else:  # New
                if task_uid is None or len(task_uid) == 0:
                    # 정보 insert
                    new_uid = new_task.create_temporary(name, task_type, owner_id, action_type)
                    rdata['task_uid'] = new_uid
                else:
                    # 정보 update
                    if new_task.update_temporary(task_uid, name, task_type, action_type, owner_id) is False:
                        flash('태스크 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
                        result['result'] = False
                    else:
                        rdata['task_uid'] = task_uid
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            flash('태스크 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
            result['result'] = False
    result['rdata'] = rdata
    result['detail'] = detail

    return jsonify(result=result)


@task_bp.route('/_check_desc', methods=['POST'])
def check_desc():
    """
    등록사유 처리
    1.형식 검사.
    2.등록 사유 저장.
    :return:
    """
    result = dict()
    rdata = dict()
    detail = dict()

    result['result'] = True
    task_uid = request.form['task_uid']
    task_type = request.form['task_type']
    desc = request.form['desc']
    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'
    # 1.형식 검사.
    current_app.logger.debug("task_uid=[%s], task_type=[%s], desc=[%s]" % (task_uid, task_type, desc))
    # task type
    c, e = check({'task_type': task_type})
    r, d = set_detail_result(c, '잘못된 형식입니다!')

    result['result'] = r if r is False else result['result']
    detail['task_type'] = d
    # desc
    c, e = check({'task_cause': desc})
    r, d = set_detail_result(c, '잘못된 형식입니다! (최소: 10자, 최대 100자)')

    result['result'] = r if r is False else result['result']
    detail['desc'] = d

    if result['result'] is True:
        try:
            task = NewTask()
            if task.update_playbook(task_uid, 0, desc, None, owner_id) is False:
                task.create_playbook(task_uid, 0, desc, None, owner_id)
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            flash('태스크 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
            result['result'] = False
    result['rdata'] = rdata
    result['detail'] = detail

    return jsonify(result=result)


@task_bp.route('/_check_script', methods=['POST'])
def check_script():
    """
    스크립트 처리
    1.금지어 체크.
    2.스크립트 저장
    :return:
    """
    result = dict()
    rdata = dict()
    detail = dict()

    result['result'] = True
    task_uid = request.form['task_uid']
    desc = request.form['desc']
    script = request.form['script']

    current_app.logger.debug("task_uid=%r" % task_uid)
    current_app.logger.debug("script=%r" % script)

    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'

    # script
    # 1.금지어 체크.
    c, e = check_forbidden_instruction(script)
    r, d = set_detail_result(c, e)

    result['result'] = r if r is False else result['result']
    detail['script'] = d
    result['rdata'] = rdata
    result['detail'] = detail
    # 2.스크립트 저장.
    if result['result'] is True:
        try:
            task = NewTask()
            if task.update_playbook(task_uid, 0, desc, script, owner_id) is False:
                task.create_playbook(task_uid, 0, desc, script, owner_id)
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            flash('태스크 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
            result['result'] = False
    return jsonify(result=result)


@task_bp.route('/_load_target_list', methods=['POST'])
def load_target_list():
    """
    스크립트 수행 목적지 출력.
    :return:
    """
    global masking
    target_list = list()
    data = request.get_json()
    current_app.logger.debug("data=%r" % data)
    task_uid = data['task_uid']

    try:
        result = TargetList.query.filter(TargetList.task_id == task_uid).all()

        for target in result:
            tmp = dict()
            tmp['Ip'] = target.host
            tmp['Port'] = str(target.port)
            tmp['Id'] = str(target.user)
            tmp['Password'] = masking

            target_list.append(tmp)
    except Exception as e:
        current_app.logger.error("!%s!" % e)

    return jsonify(result=target_list)


@task_bp.route('/_submit', methods=['POST'])
def submit():
    """
    태스크 등록 처리
    1.타겟 리스트 저장
    2.상태 변경
    :return:
    """
    global masking
    result = dict()

    result['result'] = True
    data = request.get_json()
    current_app.logger.debug("data=<%r>" % data)
    task_uid = data['task_uid']
    target_list = data['target_list']

    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'

    task = NewTask()
    # 1.타겟 리스트 저장
    try:
        for target in target_list:
            if target['Password'] != masking:
                task.update_target_list(task_uid, target['Ip'], target['Port'], target['Id'], target['Password'])
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        flash('태스크 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
        result['result'] = False
    # 2.상태 변경
    try:
        task.complete(task_uid, owner_id)
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        flash('태스크 등록 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
        result['result'] = False
    return jsonify(result=result)
