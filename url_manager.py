#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 13:57
# @Author  : yancy
# @File    : url_manager.py


class UrlManager(object):

    def __init__(self):
        # url储存在set中进行管理
        self.new_urls = set()
        self.old_urls = set()

    def add_url(self, url):
        """
        url即不在待爬取的url里面，也不在爬取过的url里面，可把该全新的url追加到新的url集合里
        :param url:
        :return:
        """
        if url is None:
            return
        elif url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
        else:
            print('falied add url: %s' % url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        else:
            for url in urls:
                self.add_url(url)

    def has_new_url(self):
        """
        判断 new urls 集合里边是否还有url
        :return: set的元素个数
        """
        len_url = len(self.new_urls)
        if len_url != 0:
            return len_url

    def get_new_url(self):
        """
        获取一个url，并返回该url
        :return:
        """
        # 在url管理列表中获取一个url，并在该列表中移除
        new_url = self.new_urls.pop()

        # 把这个被获取的url放到已爬取的url管理列表中
        self.old_urls.add(new_url)
        return new_url