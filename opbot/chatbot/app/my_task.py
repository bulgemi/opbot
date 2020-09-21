# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
from sqlalchemy import and_
from flask import current_app
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import TaskInfo, UserInfo


class MyTask(object):
    """
    사용자 테스트를 제공한다.
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
        stmt = self.__db.session.query(TaskInfo)
        stmt = stmt.with_entities(TaskInfo.task_id, TaskInfo.task_name, TaskInfo.action_type)
        task_list = stmt.filter(and_(TaskInfo.owner_id == user_id.strip(),
                                     TaskInfo.status_code == 1)).order_by(TaskInfo.action_type).all()
        return task_list

    def set_user_name(self, user_id, user_name):
        """
        사용자 ID키로 사용자 명 세팅.
        :param user_id:
        :param user_name:
        :return:
        """
        user_name_key = "user_name_{}".format(user_id)
        self.__r.rpush(user_name_key, user_name)
        return True

    def get_user_name(self, user_id):
        """
        사용자 명 반환.
        :param user_id:
        :return:
        """
        user_name_key = "user_name_{}".format(user_id)
        task_name = self.__r.lrange(user_name_key, 0, 0)
        return task_name[0].decode('utf-8')

    def del_user_name(self, user_id):
        """
        사용자 명 삭제.
        :param user_id:
        :return:
        """
        user_name_key = "user_name_{}".format(user_id)
        self.__r.delete(user_name_key)

    def set_m_tasks(self, user_id, tasks):
        """
        My Task 세팅.
        :param user_id:
        :param tasks:
        :return:
        """
        task_id_key = "task_id_{}".format(user_id)
        task_nm_key = "task_nm_{}".format(user_id)
        task_st_key = "task_st_{}".format(user_id)

        for task in tasks:
            self.__r.rpush(task_id_key, task[0])
            self.__r.rpush(task_nm_key, task[1])
            self.__r.rpush(task_st_key, 0)  # 0: None, 1: 수행 대상
        return True

    def get_m_tasks_by_id(self, user_id, task_index):
        """
        My Task 반환.
        :param user_id:
        :param task_index:
        :return task_id, task_nm, task_st:
        """
        task_id_key = "task_id_{}".format(user_id)
        task_nm_key = "task_nm_{}".format(user_id)
        task_st_key = "task_st_{}".format(user_id)

        if self.__r.llen(task_id_key) == 0 or task_index+1 > self.__r.llen(task_id_key):
            return None, None, None
        else:
            task_id = self.__r.lrange(task_id_key, task_index, task_index)
            task_nm = self.__r.lrange(task_nm_key, task_index, task_index)
            task_st = self.__r.lrange(task_st_key, task_index, task_index)
            return task_id[0].decode('utf-8'), task_nm[0].decode('utf-8'), int(task_st[0])

    def get_m_tasks_index_by_name(self, user_id, task_name):
        """
        My Task index 반환.
        :param user_id:
        :param task_name:
        :return index:
        """
        task_nm_key = "task_nm_{}".format(user_id)

        if self.__r.llen(task_nm_key) == 0 or len(task_name) == 0:
            return -1
        else:
            for i in range(0, self.__r.llen(task_nm_key)):
                task_nm = self.__r.lrange(task_nm_key, i, i)
                if task_name.strip() == task_nm[0].decode('utf-8'):
                    return i
            return -1

    def update_m_tasks(self, user_id, task_index):
        """
        My Task 상태정보 업데이트.
        :param user_id:
        :param task_index:
        :return True or False:
        """
        task_id_key = "task_id_{}".format(user_id)
        task_nm_key = "task_nm_{}".format(user_id)
        task_st_key = "task_st_{}".format(user_id)

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
            self.del_m_tasks(user_id)

            for task in tasks_info:
                self.__r.rpush(task_id_key, task[0])
                self.__r.rpush(task_nm_key, task[1])
                self.__r.rpush(task_st_key, task[2])  # 0: None, 1: 수행 대상
            return True

    def reset_run_m_task(self, user_id):
        """
        My Task 상태정보 초기화.
        :param user_id:
        :return True or False:
        """
        task_st_key = "task_st_{}".format(user_id)

        tasks_info = list()

        if self.__r.llen(task_st_key) == 0:
            return False
        else:
            for i in range(0, self.__r.llen(task_st_key)):
                tasks_info.append(0)
            self.del_m_tasks(user_id)

            for task in tasks_info:
                self.__r.rpush(task_st_key, task)  # 0: None, 1: 수행 대상
            return True

    def get_run_m_task(self, user_id):
        """
        My Task 둥 수행 대상 Task Index 번환.
        :param user_id:
        :return index:
        """
        task_st_key = "task_st_{}".format(user_id)
        for i in range(0, self.__r.llen(task_st_key)):
            task_st = self.__r.lrange(task_st_key, i, i)
            if int(task_st[0]) == 1:
                return i
        return -1

    def del_m_tasks(self, user_id):
        """
        My Task 삭제.
        :param user_id:
        :return:
        """
        task_id_key = "task_id_{}".format(user_id)
        task_nm_key = "task_nm_{}".format(user_id)
        task_st_key = "task_st_{}".format(user_id)

        self.__r.delete(task_id_key)
        self.__r.delete(task_nm_key)
        self.__r.delete(task_st_key)
