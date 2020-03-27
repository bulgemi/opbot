# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import argparse
from Crypto.PublicKey import RSA
from Crypto import Random


class FishBowl(object):
    def __init__(self):
        self.write_size = 128

    def gen_key(self):
        """
        RSA 키 생성.
        :return:
        """
        random_generator = Random.new().read
        key = RSA.generate(self.write_size * 8, random_generator)

        try:
            private_key = key.exportKey()
            file_out = open("opbot_private.pem", "wb")
            file_out.write(private_key)

            public_key = key.publickey().exportKey()
            file_out = open("opbot_public.pem", "wb")
            file_out.write(public_key)
        except ValueError as e:
            raise e
        except OSError as e:
            raise e
        except Exception as e:
            raise e
        return True

    def do_enc(self):
        import sys
        import os
        sys.path.append(os.getenv('OPBOT_HOME'))
        from manager.app.fishbowl.moss import Moss
        from manager.app.config import Config

        try:
            p = input('Enter characters to encrypt: ')
            m = Moss()
            m.load_public_key(Config.PUBLIC_KEY)
            e = m.enc(p)
            print("plain data:(%d)[%s]" % (len(p), p))
            print("Encrypted data:(%d)[%s]" % (len(e), e))
        except Exception as e:
            print(e)
            return False
        return True


if __name__ == "__main__":
    fishbowl = FishBowl()
    parser = argparse.ArgumentParser(prog='enc_tool.sh')

    parser.add_argument('-k', '--keygen', action='store_true', help='generate a RSA key(PUBLIC/PRIVATE)')
    parser.add_argument('-e', '--enc', action='store_true', help='Encrypt plain text.')
    args = parser.parse_args()

    if args.keygen is True:
        fishbowl.gen_key()
    elif args.enc is True:
        fishbowl.do_enc()
    else:
        pass
