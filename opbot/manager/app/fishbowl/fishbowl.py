# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
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


if __name__ == "__main__":
    fishbowl = FishBowl()
    fishbowl.gen_key()
