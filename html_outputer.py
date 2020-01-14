#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 13:58
# @Author  : yancy
# @File    : html_outputer.py

class HtmlOutputer(object):
    def __init__(self):
        self.data_ = []

    def collect_data(self, data):
        if data is None:
            return
        else:
            self.data_.append(data)

    def output_html(self):
        fout = open('output.html', 'w')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')

        for data in self.data_:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')

        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
