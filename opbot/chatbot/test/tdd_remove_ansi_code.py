# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import re

ansi_escape = re.compile(r'''
    \x1B    # ESC
    [@-_]   # 7-bit C1 Fe
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
''', re.VERBOSE)

result = None

with open("top.txt", "r") as f:
    data = f.read()
    result = ansi_escape.sub('', data)

with open("remove.txt", "w") as f:
    f.write(result)
