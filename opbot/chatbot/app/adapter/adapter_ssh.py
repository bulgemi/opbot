# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import os
import uuid
from fabric import Connection


class SshAdapter(object):
    def __init__(self, host, user, password, out_channel_id, port=22):
        """
        SSH Adapter 초기화
        :param host:
        :param user:
        :param password:
        :param out_channel_id:
        :param port:
        """
        dir_tmp = os.getenv('OPBOT_FILE_DIR')

        self.__conn = Connection(host=host, user=user, port=port, connect_kwargs={'password': password})
        self.__out_channel_id = out_channel_id

        if dir_tmp is not None:
            if not os.path.exists(dir_tmp):
                os.makedirs(dir_tmp)

            self.__save_dir = dir_tmp + "/"

    def do(self, command):
        """
        명령어를 원격 서버에서 수행한다.
        :param command:
        :return:
        """
        result = self.__conn.run(command)

        if result.ok is True:
            return True, result.stdout.strip()
        else:
            return False, None

    def save_file(self, src):
        """
        실행 결과를 파일로 저장.
        :param src:
        :return:
        """
        file_name = str(uuid.uuid1()) + ".txt"

        with open(self.__save_dir+file_name, 'w') as f:
            f.write(src)

        return file_name

    def delete_file(self, file_name):
        """
        실행 결과 파일 삭제.
        :param file_name:
        :return:
        """
        if os.path.isfile(self.__save_dir+file_name):
            os.remove(self.__save_dir+file_name)
