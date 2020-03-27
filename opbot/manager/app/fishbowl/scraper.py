# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from Crypto.PublicKey import RSA


class Scraper(object):
    def __init__(self):
        self.private_key = None

    def load_private_key(self, key_path):
        """
        RAS private key load
        :param key_path:
        :return:
        """
        try:
            self.private_key = RSA.importKey(open(key_path).read())
        except OSError as e:
            raise e
        except Exception as e:
            raise e
        return True

    def dec(self, enc_data):
        """
        데이터 복호화
        :param enc_data:
        :return:
        """
        offset = 0
        dec_data = b""
        enc_data_len = len(enc_data)

        while offset < enc_data_len:
            enc_block_len = int(enc_data[offset:offset+3])
            offset += 3
            enc_block = enc_data[offset:offset+enc_block_len]
            offset += enc_block_len
            piece = self.private_key.decrypt(enc_block)
            dec_data += piece
        return dec_data
