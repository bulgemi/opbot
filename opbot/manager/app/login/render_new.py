# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import (render_template, Blueprint, request, jsonify, current_app, flash, redirect, url_for)
# OPBOT manager module
from app import db
from ..validator.checker import check
from ..models import UserInfo
from .save_user import NewUser

login_bp = Blueprint('login_new', __name__)


def set_detail_result(c, msg):
    """
    checker 결과를 기반으로 상세 결과 메시지 생성.
    :param c:
    :param msg:
    :return:
    """
    detail = dict()

    if c is False:
        detail['class'] = 'validation error',
        detail['tip'] = [msg]
    else:
        detail['tip'] = ['OK']
    return c, detail


@login_bp.route('/confirm/<uid>', methods=['GET'])
def confirm(uid):
    """
    사용자 생성 화면 로딩.
    1. 계정 상태 활성화
    :return:
    """
    current_app.logger.debug("uid=<%r>" % uid)

    try:
        user = UserInfo.query.filter_by(user_id=uid).first()

        if user is None:
            flash('Confirm 실패하였습니다! 관리자에게 문의하세요!', 'error')
            return redirect(url_for('login.render'))

        current_app.logger.debug("user=<%r>", user)

        user.status_code = 1
        db.session.commit()
        flash('Confirm 완료되었습니다.', 'success')
    except Exception as e:
        current_app.logger.error("!%s!" % e)
        db.session.rollback()
        flash('Confirm 실패하였습니다! 관리자에게 문의하세요!', 'error')
    return redirect(url_for('login.render'))


@login_bp.route('/new', methods=('GET', 'POST'))
def render():
    """
    사용자 생성 화면 로딩.
    :return:
    """
    return render_template('login/user_new.html')


@login_bp.route('/_create_user', methods=['POST'])
def create_user():
    """
    사용자 생성 처리.
    1.입력값 유효성 검증.
    2.DB 저장.
    :return:
    """
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    result = dict()
    detail = dict()
    result['result'] = True

    c, e = check({'name': name})
    r, d = set_detail_result(c, '잘봇된 형식입니다! (최소: 2자, 최대 32자)')

    result['result'] = r if r is False else result['result']
    detail['name'] = d

    c, e = check({'email': email})
    r, d = set_detail_result(c, '잘못된 형식입니다! (최소 5자, 최대 150자)')

    result['result'] = r if r is False else result['result']
    detail['email'] = d

    # 2.DB 존재 여부 확인.
    if result['result'] is True:
        user = UserInfo.query.filter_by(email=email).first()

        if user is not None:
            r, d = set_detail_result(False, '존재하는 이메일입니다! (최소 5자, 최대 150자)')
            result['result'] = r if r is False else result['result']
            detail['email'] = d

    c, e = check({'password': password})
    r, d = set_detail_result(c, '잘못된 형식입니다! (특수문자/문자/숫자 포함, 최소 8자, 최대 15자)')

    result['result'] = r if r is False else result['result']
    detail['password'] = d

    result['detail'] = detail

    current_app.logger.debug("detail=<%r>" % result['detail'])

    if result['result'] is True:
        try:
            result['result_message'] = '{}님, 안녕하세요. 등록하신 e-mail로 Confirm Mail을 전송하였습니다.'.format(name)
            newbie = NewUser(name, email, password)
            newbie.create()
            newbie.send_mail()
            flash(result['result_message'], 'success')
            result['url'] = url_for('login.render', _external=True)
        except Exception as e:
            current_app.logger.error("!%s!" % e)

    return jsonify(result=result)


@login_bp.route('/_check_username', methods=['POST'])
def check_username():
    """
    사용자 이름 유효성 검사.
    1.형식 검사.
    :return:
    """
    result = dict()
    detail = dict()
    name = request.form['name']
    # 1.형식 검사.
    c, e = check({'name': name})
    result['result'] = True

    r, d = set_detail_result(c, '잘봇된 형식입니다! (최소: 2자, 최대 32자)')

    result['result'] = r if r is False else result['result']
    detail['name'] = d
    result['detail'] = detail

    return jsonify(result=result)


@login_bp.route('/_check_email', methods=['POST'])
def check_email():
    """
    이메일 유효성 검사.
    1.형식 검사.
    2.DB 존재 여부 확인.
    :return:
    """
    result = dict()
    detail = dict()
    email = request.form['email']
    # 1.형식 검사.
    c, e = check({'email': email})
    result['result'] = True

    r, d = set_detail_result(c, '잘못된 형식입니다! (최소 5자, 최대 150자)')

    result['result'] = r if r is False else result['result']
    detail['email'] = d
    result['detail'] = detail
    # 2.DB 존재 여부 확인.
    if result['result'] is True:
        user = UserInfo.query.filter_by(email=email).first()

        if user is not None:
            r, d = set_detail_result(False, '존재하는 이메일입니다! (최소 5자, 최대 150자)')
            result['result'] = r if r is False else result['result']
            detail['email'] = d
            result['detail'] = detail

    return jsonify(result=result)


@login_bp.route('/_check_password', methods=['POST'])
def check_password():
    """
    패스워드 유효성 검사
    1.형식 검사.
    :return:
    """
    result = dict()
    detail = dict()
    password = request.form['password']
    # 1.형식 검사.
    c, e = check({'password': password})
    result['result'] = True

    r, d = set_detail_result(c, '잘못된 형식입니다! (특수문자/문자/숫자 포함, 최소 8자, 최대 15자)')

    result['result'] = r if r is False else result['result']
    detail['password'] = d
    result['detail'] = detail

    return jsonify(result=result)
