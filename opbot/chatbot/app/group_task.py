# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
from flask import current_app
from sqlalchemy import and_
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import TaskInfo, UserInfo, GroupManagement


class GroupTask(object):
    """
    그룹 테스크를 제공한다.
    """
    def __init__(self, db, r):
        """
        초기화.
        :param db:
        :param r:
        """
        self.__db = db
        self.__r = r

    def get_user_id(self, slack_id):
        """
        slack id를 이용하여 user id 조회
        :param slack_id:
        :return user_id:
        """
        stmt = self.__db.session.query(UserInfo)
        stmt = stmt.with_entities(UserInfo.user_id, UserInfo.user_name)
        user_info = stmt.filter(UserInfo.slack_id == slack_id.strip()).first()
        if user_info is None:
            return None
        return user_info

    def get_list(self, user_id):
        """
        user_id를 기반으로 등록된 타스크 목록 반환.
        :param user_id:
        :return:
        """
        stmt = self.__db.session.query(GroupManagement)
        stmt = stmt.with_entities(GroupManagement.task_id)
        id_list = stmt.filter(GroupManagement.user_id == user_id.strip()).all()
        id_list = list(set(id_list))
        current_app.logger.debug("id_list=<%r>" % id_list)

        task_list = list()
        for task_id in id_list:
            stmt = self.__db.session.query(TaskInfo)
            stmt = stmt.with_entities(TaskInfo.task_id, TaskInfo.task_name, TaskInfo.action_type)
            tmp = stmt.filter(and_(TaskInfo.task_id == task_id[0],
                                   TaskInfo.status_code == 1)).first()
            if tmp is not None:
                task_list.append(tmp)
        task_list.sort(key=lambda x: x[2])
        return task_list

    def set_g_tasks(self, user_id, tasks):
        """
        Group Task 세팅.
        :param user_id:
        :param tasks:
        :return:
        """
        task_id_key = "gtask_id_{}".format(user_id)
        task_nm_key = "gtask_nm_{}".format(user_id)
        task_st_key = "gtask_st_{}".format(user_id)

        for task in tasks:
            self.__r.rpush(task_id_key, task[0])
            self.__r.rpush(task_nm_key, task[1])
            self.__r.rpush(task_st_key, 0)  # 0: None, 1: 수행 대상
        return True

    def get_g_tasks_by_id(self, user_id, task_index):
        """
        Group Task 반환.
        :param user_id:
        :param task_index:
        :return task_id, task_nm, task_st:
        """
        task_id_key = "gtask_id_{}".format(user_id)
        task_nm_key = "gtask_nm_{}".format(user_id)
        task_st_key = "gtask_st_{}".format(user_id)

        if self.__r.llen(task_id_key) == 0 or task_index+1 > self.__r.llen(task_id_key):
            return None, None, None
        else:
            task_id = self.__r.lrange(task_id_key, task_index, task_index)
            task_nm = self.__r.lrange(task_nm_key, task_index, task_index)
            task_st = self.__r.lrange(task_st_key, task_index, task_index)
            return task_id[0].decode('utf-8'), task_nm[0].decode('utf-8'), int(task_st[0])

    def get_g_tasks_index_by_name(self, user_id, task_name):
        """
        Group Task index 반환.
        :param user_id:
        :param task_name:
        :return index:
        """
        task_nm_key = "gtask_nm_{}".format(user_id)

        if self.__r.llen(task_nm_key) == 0 or len(task_name) == 0:
            return -1
        else:
            for i in range(0, self.__r.llen(task_nm_key)):
                task_nm = self.__r.lrange(task_nm_key, i, i)
                if task_name.strip() == task_nm[0].decode('utf-8'):
                    return i
            return -1

    def update_g_tasks(self, user_id, task_index):
        """
        Group Task 상태정보 업데이트.
        :param user_id:
        :param task_index:
        :return True or False:
        """
        task_id_key = "gtask_id_{}".format(user_id)
        task_nm_key = "gtask_nm_{}".format(user_id)
        task_st_key = "gtask_st_{}".format(user_id)

        tasks_info = list()

        if self.__r.llen(task_id_key) == 0 or task_index+1 > self.__r.llen(task_id_key):
            return False
        else:
            for i in range(0, self.__r.llen(task_id_key)):
                task_id = self.__r.lrange(task_id_key, i, i)
                task_nm = self.__r.lrange(task_nm_key, i, i)
                if i == task_index:
                    tasks_info.append([task_id[0].decode('utf-8'), task_nm[0].decode('utf-8'), 1])
                else:
                    tasks_info.append([task_id[0].decode('utf-8'), task_nm[0].decode('utf-8'), 0])
            self.del_g_tasks(user_id)

            for task in tasks_info:
                self.__r.rpush(task_id_key, task[0])
                self.__r.rpush(task_nm_key, task[1])
                self.__r.rpush(task_st_key, task[2])  # 0: None, 1: 수행 대상
            return True

    def reset_run_g_task(self, user_id):
        """
        Group Task 상태정보 초기화.
        :param user_id:
        :return True or False:
        """
        task_st_key = "gtask_st_{}".format(user_id)

        tasks_info = list()

        if self.__r.llen(task_st_key) == 0:
            return False
        else:
            for i in range(0, self.__r.llen(task_st_key)):
                tasks_info.append(0)
            self.del_g_tasks(user_id)

            for task in tasks_info:
                self.__r.rpush(task_st_key, task)  # 0: None, 1: 수행 대상
            return True

    def get_run_g_task(self, user_id):
        """
        Group Task 둥 수행 대상 Task Index 번환.
        :param user_id:
        :return index:
        """
        task_st_key = "gtask_st_{}".format(user_id)
        for i in range(0, self.__r.llen(task_st_key)):
            task_st = self.__r.lrange(task_st_key, i, i)
            if int(task_st[0]) == 1:
                return i
        return -1

    def del_g_tasks(self, user_id):
        """
        Group Task 삭제.
        :param user_id:
        :return:
        """
        task_id_key = "gtask_id_{}".format(user_id)
        task_nm_key = "gtask_nm_{}".format(user_id)
        task_st_key = "gtask_st_{}".format(user_id)

        self.__r.delete(task_id_key)
        self.__r.delete(task_nm_key)
        self.__r.delete(task_st_key)
