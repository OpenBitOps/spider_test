#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/11 13:58
# @Author  : yancy
# @File    : html_downloader.py

from urllib.request import urlopen
'''
#print(response.read().decode('utf-8'))   #返回网页内容
#print(response.getheader('server')) #返回响应头中的server值
#print(response.getheaders()) #以列表元祖对的形式返回响应头信息
#print(response.fileno()) #返回文件描述符
#print(response.version)  #返回版本信息
#print(response.status)  #返回状态码200，404代表网页未找到
#print(response.debuglevel) #返回调试等级
#print(response.closed)  #返回对象是否关闭布尔值
#print(response.geturl()) #返回检索的URL
#print(response.info()) #返回网页的头信息
#print(response.getcode()) #返回响应的HTTP状态码
#print(response.msg)  #访问成功则返回ok
#print(response.reason) #返回状态信息
'''

class HtmlDownlaoder(object):
    def download(self, url):
        if url is None:
            return None
        else:
            resp = urlopen(url)
            if resp.status != 200:
                print('failed to %s (get method)' % url)
                return None
            else:
                return resp.read()