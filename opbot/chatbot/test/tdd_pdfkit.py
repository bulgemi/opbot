# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import pdfkit

pdfkit.from_url('http://google.com', 'google.pdf')
pdfkit.from_string('hello<br/>hello', 'hello.pdf')
pdfkit.from_file('top.txt', 'top.pdf')
pdfkit.from_file('b099220d-f56a-11e9-b5df-d0abd5335702.txt',
                 'b099220d-f56a-11e9-b5df-d0abd5335702.pdf')

with open("top.txt", "r") as f:
    data = ""
    while True:
        line = f.readline()
        if not line:
            break
        data += line + "<br/>"
    pdfkit.from_string(data, 'top2.pdf')
