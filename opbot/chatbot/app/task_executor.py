# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
요청된 Task 수행.
"""
import sys
import os
import uuid
from time import sleep
from flask import current_app
from sqlalchemy import and_
from pdfkit import from_file as pdfkit_ff
sys.path.append(os.getenv('OPBOT_HOME'))
from manager.app.models import TargetList, TaskInfo


class TaskExecutor(object):
    def __init__(self, task_id, out_channel_id, db):
        """
        Task Executor 생성.
        :param task_id:
        :param out_channel_id:
        :param db:
        """
        dir_tmp = os.getenv('OPBOT_FILE_DIR')

        if dir_tmp is not None:
            if not os.path.exists(dir_tmp):
                os.makedirs(dir_tmp)
            self.__save_dir = dir_tmp + "/"

        self.__task_id = task_id.strip()
        self.__out_channel_id = out_channel_id.strip()
        self.__db = db

    def report_generate(self, org_file, pdf_file):
        """
        PDF 보고서 생성.
        :param org_file:
        :param pdf_file:
        :return: True on Success
        """
        return pdfkit_ff(self.__save_dir+org_file, self.__save_dir+pdf_file)

    def run_task(self):
        """
        1.task 수행.
        2.결과 수신.
        3.pdf 생성.
        4.파일 첨부.
        :return:
        """
        current_app.bot.put_broadcast(channel=self.__out_channel_id,
                                      message="[{}] 수행합니다.".format(self.__task_id))

        stmt = self.__db.session.query(TargetList)
        stmt = stmt.with_entities(TargetList.host,
                                  TargetList.port,
                                  TargetList.user,
                                  TargetList.passwd,
                                  TargetList.adapter_type)
        target_info = stmt.filter(and_(TargetList.task_id == self.__task_id,
                                       TargetList.out_channel_id == self.__out_channel_id)).first()

        if target_info.adapter_type == 0:
            # SSH Adapter
            from .adapter.adapter_ssh import SshAdapter
            ssh_adapter = SshAdapter(target_info.host,
                                     target_info.user,
                                     target_info.passwd,
                                     self.__out_channel_id,
                                     target_info.port)
            # task_info 조회
            stmt = self.__db.session.query(TaskInfo)
            stmt = stmt.with_entities(TaskInfo.task_type,
                                      TaskInfo.script)
            tasks_info = stmt.filter(TaskInfo.task_id == self.__task_id).order_by(TaskInfo.script_seq.asc()).all()

            for task_info in tasks_info:
                if task_info[0] == 'c':
                    # 명령어 수행.
                    result, out = ssh_adapter.do(task_info[1])

                    if result is True:
                        pdf_file = str(uuid.uuid1()) + ".pdf"
                        org_file = ssh_adapter.save_file(out)
                        # txt 파일 삭제, todo: 파일 안 지워짐!!
                        ssh_adapter.delete_file(out)
                else:
                    pass

                # pdf 파일 생성.
                current_app.bot.put_broadcast(channel=self.__out_channel_id,
                                              message="[{}] 보고서 생성 중입니다.".format(self.__task_id))
                try:
                    self.report_generate(org_file, pdf_file)
                except OSError as err:
                    current_app.logger.debug("OS Error: %s" % err)

                current_app.bot.upload_report(self.__out_channel_id,
                                              self.__save_dir+pdf_file,
                                              self.__task_id)

            current_app.bot.put_broadcast(channel=self.__out_channel_id,
                                          message="[{}] 완료하였습니다.".format(self.__task_id))
            current_app.bot.choose_as(channel=self.__out_channel_id)
        else:
            pass
        pass
