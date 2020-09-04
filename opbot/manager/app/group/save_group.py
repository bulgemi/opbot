# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from flask import current_app
# manager module
from app import db
from ..models import GroupInfo, GroupManagement, TaskInfo


class NewGroup(object):
    def __init__(self):
        """
        그룹 생성 초기화
        """
        pass

    def create_new(self, group_name, owner_id):
        """
        그룹 생성.
        :param group_name:
        :param owner_id:
        :return:
        """
        from datetime import datetime
        from uuid import uuid1

        group_id = 'g_' + str(uuid1())
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')

        try:
            new_group = GroupInfo(
                group_id=group_id,
                group_name=group_name,
                owner_id=owner_id,
                create_time=current_time,
                update_time=current_time,
                audit_id=owner_id
            )
            db.session.add(new_group)
            db.session.commit()

            return group_id
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            raise e

    def update_group(self, group_id, group_name, audit_id):
        """
        그룹 수정.
        :param group_id:
        :param group_name:
        :param audit_id:
        :return:
        """
        from datetime import datetime
        current_app.logger.debug("group_id=<%r>" % group_id)

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            group_info = GroupInfo.query.filter_by(group_id=group_id).first()

            if group_info is None:
                return False
            group_info.group_name = group_name
            group_info.update_time = current_time
            group_info.audit_id = audit_id

            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            return False
        return True

    def get_task_info(self, task_id):
        """
        task 소유자 정보 반환.
        :param task_id:
        :return:
        """
        try:
            task_info = TaskInfo.query.filter_by(task_id=task_id).first()

            if task_info is None:
                return None
            else:
                return task_info.owner_id
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            raise e

    def update_group_management(self, group_id, task_infos, audit_id):
        """
        그룹 Task 정보 저장.
        :param group_id:
        :param task_infos:
        :param audit_id:
        :return:
        """
        from datetime import datetime

        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        # 그룹 멤버/Task 정보 삭제.
        try:
            group_info = GroupManagement.query.filter_by(group_id=group_id).all()
            db.session.delete(group_info)
            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            return False

        # 그룹 멤버/Task 정보 저장.
        try:
            for task_info in task_infos:
                new_group_management = GroupManagement(
                    group_id=group_id,
                    user_id=task_info['user_id'],
                    task_id=task_info['task_id'],
                    create_time=current_time,
                    update_time=current_time,
                    audit_id=audit_id
                )
                db.session.add(new_group_management)
            db.session.commit()
        except Exception as e:
            current_app.logger.error("!%s!" % e)
            db.session.rollback()
            return False
        return True
