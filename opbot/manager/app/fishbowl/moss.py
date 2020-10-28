# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class Moss(object):
    def __init__(self):
        self.public_key = None
        self.read_size = 86

    def load_public_key(self, key_path):
        """
        RAS public key load
        :param key_path:
        :return:
        """
        try:
            key = RSA.importKey(open(key_path).read())
            self.public_key = PKCS1_OAEP.new(key)
        except OSError as e:
            raise e
        except Exception as e:
            raise e
        return True

    def __split_len(self, data, length):
        """
        암호화/복호화 크기별 데이터 split
        :param data:
        :param length:
        :return:
        """
        return [data[i:i+length] for i in range(0, len(data), length)]

    def enc(self, plain_data):
        """
        데이터 암호화
        :param plain_data:
        :return:
        """
        enc_blocks = self.__split_len(plain_data.encode('utf-8'), self.read_size)
        enc_data = b""

        for tmp in enc_blocks:
            piece = self.public_key.encrypt(tmp)
            ln = "{:03d}".format(len(piece))
            buf = ln.encode('utf-8') + piece
            enc_data += buf
        return enc_data
