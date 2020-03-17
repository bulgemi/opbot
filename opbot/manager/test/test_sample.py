# content of test_sample.py
def inc(x):
    return x + 1


def test_answer_false():
    assert inc(3) == 5


def test_answer_true():
    assert inc(3) == 4
