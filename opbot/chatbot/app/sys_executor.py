# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
"""
요청된 Task 수행.
"""
import sys
import os
from flask import current_app
from pdfkit import from_file as pdfkit_ff
sys.path.append(os.getenv('OPBOT_HOME'))


class SysExecutor(object):
    def __init__(self, db, out_channel_id, node_list):
        """
        시스템 Executor 생성.
        :param db:
        :param out_channel_id:
        :param node_list:
        """
        self.__out_channel_id = out_channel_id.strip()
        self.__db = db
        self.__node_list = node_list

    def report_generate(self, org_file, pdf_file):
        """
        PDF 보고서 생성.
        :param org_file:
        :param pdf_file:
        :return: True on Success
        """
        return pdfkit_ff(self.__save_dir+org_file, self.__save_dir+pdf_file)

    def run_cpu_task(self):
        """
        1.task 수행.
        2.결과 수신.
        3.파일 첨부.
        :return:
        """
        from .sys_report_generator import SysReportGenerator

        message = "{} 노드에 대한 CPU 사용량 분석 수행합니다.".format(str(self.__node_list))
        current_app.bot.put_broadcast(channel=self.__out_channel_id, message=message)

        sys_report_gen = SysReportGenerator()
        chart_file = sys_report_gen.cpu_report(self.__node_list)
        table_file = sys_report_gen.cpu_table(self.__node_list)

        message = "{} 노드에 대한 CPU 사용량 보고서 생성 중입니다.".format(str(self.__node_list))
        current_app.bot.put_broadcast(channel=self.__out_channel_id, message=message)

        current_app.bot.upload_report(self.__out_channel_id, chart_file, "CPU 사용량 그래프 보고서")
        current_app.bot.upload_report(self.__out_channel_id, table_file, "CPU 사용량 상세 보고서")

        message = "{} 노드에 대한 CPU 사용량 보고서 완료하였습니다.".format(str(self.__node_list))
        current_app.bot.put_broadcast(channel=self.__out_channel_id, message=message)

    def run_mem_task(self):
        """
        1.task 수행.
        2.결과 수신.
        3.파일 첨부.
        :return:
        """
        from .sys_report_generator import SysReportGenerator

        message = "{} 노드에 대한 Memory 사용량 분석 수행합니다.".format(str(self.__node_list))
        current_app.bot.put_broadcast(channel=self.__out_channel_id, message=message)

        sys_report_gen = SysReportGenerator()
        chart_file = sys_report_gen.mem_report(self.__node_list)
        table_file = sys_report_gen.mem_table(self.__node_list)

        message = "{} 노드에 대한 Memory 사용량 보고서 생성 중입니다.".format(str(self.__node_list))
        current_app.bot.put_broadcast(channel=self.__out_channel_id, message=message)

        current_app.bot.upload_report(self.__out_channel_id, chart_file, "Memory 사용량 그래프 보고서")
        current_app.bot.upload_report(self.__out_channel_id, table_file, "Memory 사용량 상세 보고서")

        message = "{} 노드에 대한 Memory 사용량 보고서 완료하였습니다.".format(str(self.__node_list))
        current_app.bot.put_broadcast(channel=self.__out_channel_id, message=message)
