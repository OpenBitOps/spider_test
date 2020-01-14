#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 13:06
# @Author  : yancy
# @File    : main.py

from url_manager import UrlManager
from html_downloader import HtmlDownlaoder
from html_parser import HtmlParser
from html_outputer import HtmlOutputer

class SpiderMain(object):
    def __init__(self):
        self.urls = UrlManager()
        self.downlaoder = HtmlDownlaoder()
        self.parser = HtmlParser()
        self.outputer = HtmlOutputer()

    def craw(self, root_url):
        count = 1
        # 把根url 传入url管理列表
        self.urls.add_url(root_url)

        # 页面爬取循环程序
        while self.urls.has_new_url():
            try:
                # 获取一个待爬取的url
                new_url = self.urls.get_new_url()
                print('craw %d: %s' % (count, new_url))

                # 下载该url爬取context
                html_cont = self.downlaoder.download(new_url)

                # 通过解析器，解析该url下载到的内容，获取新的 new_urls 和 新的 data
                new_urls, new_data = self.parser.parse(new_url, html_cont)

                # 把获取到 新的url添加到新的url管理器，
                self.urls.add_new_urls(new_urls)

                # 把获取的新的data添加到新的数据处理器中
                self.outputer.collect_data(new_data)

                if count == 100:
                    break

                count += 1
            except Exception as e:
                print('craw failed')

        self.outputer.output_html()

if __name__ == '__main__':
    root_url = 'http://baike.baidu.com/view/21087.htm'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)