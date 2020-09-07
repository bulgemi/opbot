# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, request, jsonify, current_app, flash)
# manager module
from ..models import GroupInfo, GroupManagement, UserInfo, TaskInfo
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
            if GroupInfo.query.filter_by(group_name=group_name).first() is not None:
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


@group_bp.route('/_check_group_member', methods=['POST'])
def check_group_member():
    """
    그룹 멤보 정보를 조회 후 관련 정보를 반환한다.
    1.형식 검사.
    2.정보 조회.
    3.정보 조립.
        - 이름
        - ID
        - TASK
    :return:
    """
    result = dict()
    detail = dict()
    members = list()

    result['result'] = True
    member_info = request.form['member_info']
    member_info = member_info.strip()  # 좌/우 공백 제거.

    current_app.logger.debug("member_info=[%s]" % member_info)

    # 1.형식 검사.
    c, e = check({'member_info': member_info})
    r, d = set_detail_result(c, '멤버 이름은 최소 2자, 최대 5자입니다!')
    result['result'] = r if r is False else result['result']
    detail['member_infos'] = d

    # 2.정보 조회.
    if result['result'] is True:
        try:
            users = UserInfo.query.filter_by(user_name=member_info).all()

            for user in users:
                """
                3.정보 조립.
                - 이름
                - ID
                - TASK
                """
                tasks = TaskInfo.query.filter_by(owner_id=user.user_id).all()

                task_info = list()
                for task in tasks:
                    task_info.append({'task_id': task.task_id,
                                      'task_name': task.task_name})
                members.append({'name': user.user_name,
                                'email': user.email,
                                'task_info': task_info})
            detail['members'] = members

            current_app.logger.debug("len(users)=<%r>" % len(users))
            if len(users) == 0:
                r, d = set_detail_result(False, '멤버 정보가 없습니다!')
                result['result'] = r if r is False else result['result']
                detail['member_infos'] = d

            current_app.logger.debug("members=<%r>" % members)
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            flash('그룹 멤버 처리에 실패하였습니다! 관리자에게 문의하세요!', 'error')
            result['result'] = False
    result['detail'] = detail
    return jsonify(result=result)


@group_bp.route('/_submit', methods=['POST'])
def submit():
    """
    그룹 등록 처리
    1.그룹명 저장
    2.그룹 멤버/Task 저장
    :return:
    """
    from .save_group import NewGroup

    new_group = NewGroup()
    result = dict()

    result['result'] = True
    data = request.get_json()
    current_app.logger.debug("data=<%r>" % data)
    if 'group_id' in data:
        group_id = data['group_id']
    else:
        group_id = None
    group_name = data['group_name']
    member_list = data['member_list']
    task_list = data['task_list']
    # user email to user id
    try:
        member_list = [new_group.get_user_id(email) for email in member_list]
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        result['result'] = False
    # member 중복 제거
    member_list = list(set(member_list))

    # Todo: login 처리 후 login_id 사용하도록 수정 필요, add 2020.04.22. kim dong-hun
    owner_id = 'u_425690ee-6fff-11ea-8634-d0abd5335702'

    # 1.그룹명 저장
    try:
        if group_id is None:
            group_id = new_group.create_new(group_name, owner_id)
        else:
            new_group.update_group(group_id, group_name, owner_id)
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        result['result'] = False
    # 2.그룹 멤버/Task 저장
    task_infos = list()
    try:
        for task in task_list:
            tmp = dict()
            tmp['task_id'] = task
            tmp['user_id'] = new_group.get_task_info(task)
            task_infos.append(tmp)

            try:
                member_list.remove(tmp['user_id'])
            except ValueError:
                pass
            except Exception as e:
                current_app.logger.error("!%s!" % e)
                raise e

        current_app.logger.debug("task_infos=<%r>" % task_infos)
        new_group.update_group_management(group_id, task_infos, owner_id)
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        result['result'] = False

    try:
        new_group.update_group_management_member(group_id, member_list, owner_id)
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        result['result'] = False

    return jsonify(result=result)
