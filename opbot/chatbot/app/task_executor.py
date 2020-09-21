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
# from manager.app.models import TargetList, TaskInfo, TaskPlaybook


class TaskExecutor(object):
    def __init__(self, db, task_id, out_channel_id, task_name, task_type, target_list, contents, exe_type):
        """
        Task Executor 생성.
        :param db:
        :param task_id:
        :param out_channel_id:
        :param task_name:
        :param task_type:
        :param target_list:
        :param contents:
        :param exe_type:
        """
        dir_tmp = os.getenv('OPBOT_FILE_DIR')

        if dir_tmp is not None:
            if not os.path.exists(dir_tmp):
                os.makedirs(dir_tmp)
            self.__save_dir = dir_tmp + "/"

        self.__task_id = task_id.strip()
        self.__out_channel_id = out_channel_id.strip()
        self.__db = db
        self.__task_name = task_name
        self.__task_type = task_type
        self.__target_list = target_list
        self.__contents = contents
        self.__exe_type = exe_type

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
                                      message="[{}] 수행합니다.".format(self.__task_name))

        from .adapter.adapter_ssh import SshAdapter
        for target in self.__target_list:
            if target[4] == 0:
                # SSH Adapter
                ssh_adapter = SshAdapter(target[0],  # host
                                         target[2],  # user
                                         target[3],  # passwd
                                         self.__out_channel_id,
                                         target[1])  # port

                if self.__task_type == 1 or self.__task_type == 2 or self.__task_type == 3:
                    # 명령어 수행.
                    result, out = ssh_adapter.do(self.__contents)

                    if result is True:
                        pdf_file = str(uuid.uuid1()) + ".pdf"
                        org_file = ssh_adapter.save_file(out)
                        # txt 파일 삭제, todo: 파일 안 지워짐!!
                        ssh_adapter.delete_file(out)
                    else:
                        pass

                    # pdf 파일 생성.
                    current_app.bot.put_broadcast(channel=self.__out_channel_id,
                                                  message="[{}] 보고서 생성 중입니다.".format(self.__task_name))
                    try:
                        self.report_generate(org_file, pdf_file)
                    except OSError as err:
                        current_app.logger.debug("OS Error: %s" % err)

                    current_app.bot.upload_report(self.__out_channel_id,
                                                  self.__save_dir+pdf_file,
                                                  self.__task_name)

                    current_app.bot.put_broadcast(channel=self.__out_channel_id,
                                                  message="[{}] 완료하였습니다.".format(self.__task_name))
                    if self.__exe_type == 0:
                        current_app.bot.choose_as(channel=self.__out_channel_id)
                else:
                    pass
            else:
                pass
