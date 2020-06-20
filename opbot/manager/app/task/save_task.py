# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
# OPBOT manager module
from app import db
from ..models import TaskInfo, TaskPlaybook, TargetList


class NewTask(object):
    def __init__(self):
        """
        태스크 생성 초기화.
        """
        pass

    def create_temporary(self, task_name, task_type, owner_id, action_type):
        """
        태스크 생성.
        :param task_name:
        :param task_type:
        :param owner_id:
        :param action_type:
        :return: task uid
        """
        from datetime import datetime
        from uuid import uuid1

        task_id = 't_' + str(uuid1())
        task_name = task_name
        status_code = 3  # 0(abnormal)/1(normal)/2(lock)/3(temporary)

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            tmp_task = TaskInfo(
                task_id=task_id,
                task_name=task_name,
                task_type=task_type,
                owner_id=owner_id,
                action_type=action_type,
                status_code=status_code,
                create_time=current_time,
                update_time=current_time,
                audit_id=owner_id
            )
            db.session.add(tmp_task)
            db.session.commit()

            return task_id
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            raise e

    def update_temporary(self, task_id, task_name, task_type, action_type, audit_id):
        """
        태스크 update.
        :param task_id:
        :param task_name:
        :param task_type:
        :param action_type:
        :param audit_id:
        :return:
        """
        from datetime import datetime
        current_app.logger.debug("task_id=<%r>" % task_id)

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            task = TaskInfo.query.filter_by(task_id=task_id).first()

            if task is None:
                return False
            task.task_name = task_name
            task.task_type = task_type
            task.action_type = action_type
            task.update_time = current_time
            task.audit_id = audit_id

            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
        return True

    def complete(self, task_id, audit_id):
        """
        태스크 완료.
        :param task_id:
        :param audit_id:
        :return:
        """
        from datetime import datetime
        current_app.logger.debug("task_id=<%r>" % task_id)

        status_code = 1  # 0(abnormal)/1(normal)/2(lock)/3(temporary)
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            task = TaskInfo.query.filter_by(task_id=task_id).first()

            if task is None:
                return False
            task.update_time = current_time
            task.status_code = status_code,
            task.audit_id = audit_id

            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
        return True

    def create_playbook(self, task_id, seq, desc, script, audit_id):
        """
        create playbook.
        :param task_id:
        :param seq:
        :param desc:
        :param script:
        :param audit_id:
        :return:
        """
        from datetime import datetime

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            if script is not None:
                # 암호화
                moss = current_app.config['MOSS']
                tmp_playbook = TaskPlaybook(
                    task_id=task_id,
                    task_seq=seq,
                    contents=moss.enc(script),
                    cause=desc,
                    create_time=current_time,
                    update_time=current_time,
                    audit_id=audit_id
                )
            else:
                tmp_playbook = TaskPlaybook(
                    task_id=task_id,
                    task_seq=seq,
                    cause=desc,
                    create_time=current_time,
                    update_time=current_time,
                    audit_id=audit_id
                )
            db.session.add(tmp_playbook)
            db.session.commit()

            return True
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            raise e

    def update_playbook(self, task_id, seq, desc, script, audit_id):
        """
        update playbook.
        :param task_id:
        :param seq:
        :param desc:
        :param script:
        :param audit_id:
        :return:
        """
        from datetime import datetime
        from sqlalchemy import and_

        current_app.logger.debug("task_id=<%r>" % task_id)

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            playbook = TaskPlaybook.query.filter(and_(TaskPlaybook.task_id == task_id,
                                                      TaskPlaybook.task_seq == seq)).first()

            if playbook is None:
                return False
            playbook.cause = desc
            # 암호화
            if script is not None:
                moss = current_app.config['MOSS']
                playbook.contents = moss.enc(script)
            playbook.update_time = current_time
            playbook.audit_id = audit_id

            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
        return True

    def update_target_list(self, task_id, host, port, user, password, out_channel_id="#opbot_swing", adapter_type=0):
        """
        create the target list
        :param task_id:
        :param host:
        :param port:
        :param user:
        :param password:
        :param out_channel_id:
        :param adapter_type:
        :return:
        """
        from sqlalchemy import and_

        current_app.logger.debug("task_id=<%r>" % task_id)
        current_app.logger.debug("host=<%r>" % host)
        current_app.logger.debug("port=<%r>" % port)
        current_app.logger.debug("user=<%r>" % user)
        current_app.logger.debug("password=<%r>" % password)

        try:
            target = TargetList.query.filter(and_(TargetList.task_id == task_id,
                                                  TargetList.host == host,
                                                  TargetList.port == port,
                                                  TargetList.user == user,
                                                  TargetList.adapter_type == adapter_type,
                                                  TargetList.out_channel_id == out_channel_id)).first()
            moss = current_app.config['MOSS']
            if target is not None:
                target.passwd = moss.enc(password)
            else:
                new_target = TargetList(
                    task_id=task_id,
                    host=host,
                    port=port,
                    user=user,
                    passwd=moss.enc(password),
                    out_channel_id=out_channel_id,
                    adapter_type=adapter_type
                )
                db.session.add(new_target)
            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
        return True
