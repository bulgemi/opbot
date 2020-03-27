# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import sys
import os
sys.path.append(os.getenv('OPBOT_HOME'))


def test_gen_key():
    """
    RSA 키 생성
    :return:
    """
    from manager.app.fishbowl.fishbowl import FishBowl

    fishbowl = FishBowl()
    assert fishbowl.gen_key() is True


def test_load_private_key():
    """
    private key 로드
    :return:
    """
    from manager.app.fishbowl.scraper import Scraper
    scraper = Scraper()
    key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_private.pem"
    assert scraper.load_private_key(key_path) is True


def test_load_public_key():
    """
    public key 로드
    :return:
    """
    from manager.app.fishbowl.moss import Moss
    moss = Moss()
    key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_public.pem"
    assert moss.load_public_key(key_path) is True


def test_enc_dec_short():
    """
    단문 암호화/복호화 테스트
    :return:
    """
    from manager.app.fishbowl.moss import Moss
    from manager.app.fishbowl.scraper import Scraper
    moss = Moss()
    scraper = Scraper()
    test_set = [
        "kim dong-hun",
        "김동훈",
        "donghun_kim@sk.com",
        "가나다라마바사아자차카타파하",
        "가나다라마바사아자차카타파하0123456789",
        "가나다라마바사아자차카타파하0123456789!@#$%^&*()_+-=",
        "01234567890123456789012345678901234567890123456789",
        "0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789",
    ]
    private_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_private.pem"
    public_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_public.pem"

    assert scraper.load_private_key(private_key_path) is True
    assert moss.load_public_key(public_key_path) is True

    print("- begin")
    for test in test_set:
        enc_result = moss.enc(test)
        print("enc=(%d)[%s]" % (len(enc_result), enc_result))
        dec_result = scraper.dec(enc_result)
        print("dec=(%d)[%s]" % (len(dec_result), dec_result))


def test_enc_dec_long_kor():
    """
    장문 암호화/복호화 테스트
    :return:
    """
    from manager.app.fishbowl.moss import Moss
    from manager.app.fishbowl.scraper import Scraper
    moss = Moss()
    scraper = Scraper()
    test_data = """
황순원(1915∼2000)의 소설 ‘소나기’의 속편(이미 만들어진 소설, 영화의 뒷이야기)이 후배 소설가들에 의해 써진다.
최근 대산문화재단에 따르면 전상국, 박덕규 등 소설가 5명이 황순원 탄생 100주년을 맞아 황순원에 대한 존경의 표시로 ‘소나기’ 속편을 선보인다. 소설가들이 각각 쓴 작품 5편은 문학 계간지(계절에 따라 한 해에 네 번씩 발행하는 잡지) ‘대산문화’ 여름호(6월 발행)에 실릴 예정.
농촌을 배경으로 도시에서 온 소녀와 시골 소년의 애틋한 감정을 담은 소나기는 우리나라에서 가장 대중적이고 서정적인 소설로 꼽힌다.
줄거리는 다음과 같다. 우연히 만난 소년과 소녀는 소나기를 만나 비를 피한다. 소녀와 헤어진 소년은 이날 맞은 소나기 때문에 소녀가 병에 걸려 세상을 떠났다는 이야기를 뒤늦게 듣고 슬퍼한다.
5명의 소설가들은 상상력을 발휘해 이 뒤에 이어질 이야기를 쓴 5개의 속편을 내놓는다.
    """
    test_data_eng = """
Python is an easy to learn, powerful programming language.
It has efficient high-level data structures and a simple but effective approach to object-oriented programming.
Python’s elegant syntax and dynamic typing, together with its interpreted nature,
make it an ideal language for scripting and rapid application development in many areas on most platforms.
The Python interpreter and the extensive standard library are freely available in source or binary
form for all major platforms from the Python Web site,
https://www.python.org/, and may be freely distributed.
The same site also contains distributions of and pointers to many free third party Python modules, programs and tools,
and additional documentation.
The Python interpreter is easily extended with new functions and data types implemented in C or C++
(or other languages callable from C).
Python is also suitable as an extension language for customizable applications.
This tutorial introduces the reader informally to the basic concepts and features of the Python language and system.
It helps to have a Python interpreter handy for hands-on experience, but all examples are self-contained,
so the tutorial can be read off-line as well.
For a description of standard objects and modules, see The Python Standard Library.
The Python Language Reference gives a more formal definition of the language.
To write extensions in C or C++, read Extending and Embedding the Python Interpreter and Python/C API Reference Manual.
There are also several books covering Python in depth.
This tutorial does not attempt to be comprehensive and cover every single feature, or even every commonly used feature.
Instead, it introduces many of Python’s most noteworthy features,
and will give you a good idea of the language’s flavor and style.
After reading it, you will be able to read and write Python modules and programs,
and you will be ready to learn more about the various Python library modules described in The Python Standard Library.
    """
    private_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_private.pem"
    public_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_public.pem"

    assert scraper.load_private_key(private_key_path) is True
    assert moss.load_public_key(public_key_path) is True

    print("- begin(%d)" % len(test_data))
    enc_result = moss.enc(test_data)
    print("enc=(%d)[%s]" % (len(enc_result), enc_result))
    dec_result = scraper.dec(enc_result)
    print("dec=(%d)[%s]" % (len(dec_result), dec_result))


def test_enc_dec_long_kor():
    """
    장문 암호화/복호화 테스트
    :return:
    """
    from manager.app.fishbowl.moss import Moss
    from manager.app.fishbowl.scraper import Scraper
    moss = Moss()
    scraper = Scraper()
    test_data = """
황순원(1915∼2000)의 소설 ‘소나기’의 속편(이미 만들어진 소설, 영화의 뒷이야기)이 후배 소설가들에 의해 써진다.
최근 대산문화재단에 따르면 전상국, 박덕규 등 소설가 5명이 황순원 탄생 100주년을 맞아 황순원에 대한 존경의 표시로 ‘소나기’ 속편을 선보인다. 소설가들이 각각 쓴 작품 5편은 문학 계간지(계절에 따라 한 해에 네 번씩 발행하는 잡지) ‘대산문화’ 여름호(6월 발행)에 실릴 예정.
농촌을 배경으로 도시에서 온 소녀와 시골 소년의 애틋한 감정을 담은 소나기는 우리나라에서 가장 대중적이고 서정적인 소설로 꼽힌다.
줄거리는 다음과 같다. 우연히 만난 소년과 소녀는 소나기를 만나 비를 피한다. 소녀와 헤어진 소년은 이날 맞은 소나기 때문에 소녀가 병에 걸려 세상을 떠났다는 이야기를 뒤늦게 듣고 슬퍼한다.
5명의 소설가들은 상상력을 발휘해 이 뒤에 이어질 이야기를 쓴 5개의 속편을 내놓는다.
    """

    private_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_private.pem"
    public_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_public.pem"

    assert scraper.load_private_key(private_key_path) is True
    assert moss.load_public_key(public_key_path) is True

    print("- begin(%d)" % len(test_data))
    enc_result = moss.enc(test_data)
    print("enc=(%d)[%s]" % (len(enc_result), enc_result))
    dec_result = scraper.dec(enc_result)
    print("dec=(%d)[%s]" % (len(dec_result), dec_result))


def test_enc_dec_long_eng():
    """
    장문 암호화/복호화 테스트
    :return:
    """
    from manager.app.fishbowl.moss import Moss
    from manager.app.fishbowl.scraper import Scraper
    moss = Moss()
    scraper = Scraper()
    test_data = """
Python is an easy to learn, powerful programming language.
It has efficient high-level data structures and a simple but effective approach to object-oriented programming.
Python’s elegant syntax and dynamic typing, together with its interpreted nature,
make it an ideal language for scripting and rapid application development in many areas on most platforms.
The Python interpreter and the extensive standard library are freely available in source or binary
form for all major platforms from the Python Web site,
https://www.python.org/, and may be freely distributed.
The same site also contains distributions of and pointers to many free third party Python modules, programs and tools,
and additional documentation.
The Python interpreter is easily extended with new functions and data types implemented in C or C++
(or other languages callable from C).
Python is also suitable as an extension language for customizable applications.
This tutorial introduces the reader informally to the basic concepts and features of the Python language and system.
It helps to have a Python interpreter handy for hands-on experience, but all examples are self-contained,
so the tutorial can be read off-line as well.
For a description of standard objects and modules, see The Python Standard Library.
The Python Language Reference gives a more formal definition of the language.
To write extensions in C or C++, read Extending and Embedding the Python Interpreter and Python/C API Reference Manual.
There are also several books covering Python in depth.
This tutorial does not attempt to be comprehensive and cover every single feature, or even every commonly used feature.
Instead, it introduces many of Python’s most noteworthy features,
and will give you a good idea of the language’s flavor and style.
After reading it, you will be able to read and write Python modules and programs,
and you will be ready to learn more about the various Python library modules described in The Python Standard Library.
    """

    private_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_private.pem"
    public_key_path = "/home/donghun/PycharmProjects/opbot/opbot/manager/test/opbot_public.pem"

    assert scraper.load_private_key(private_key_path) is True
    assert moss.load_public_key(public_key_path) is True

    print("- begin(%d)" % len(test_data))
    enc_result = moss.enc(test_data)
    print("enc=(%d)[%s]" % (len(enc_result), enc_result))
    dec_result = scraper.dec(enc_result)
    print("dec=(%d)[%s]" % (len(dec_result), dec_result))
