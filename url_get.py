#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/19 9:59
# @Author  : Ethan
# @File    : url_get.py

import re
import requests
from bs4 import BeautifulSoup
import json
import jsonpath
import time
import urllib3

class nifty_information_get():
    def __init__(self, root_url):
        self.root_url = root_url

    def url_get(self):
        url_object = self.root_url
        headers = {
            'authority': 'pfs.nifcloud.com',
            'scheme': 'https',
            'accept-encoding': 'gzip, deflate, br',
            'user-agent': 'Mozilla/5.0(WindowsNT10.0; Win64; x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/79.0.3945.117 Safari/537.36'
        }
        urllib3.disable_warnings()
        info = requests.get(url=url_object, headers=headers, verify=False)
        url_context = info.text
        return url_context

    def url_context_handle(self):
        # 将获取url的内容处理成一个dict格式，再转化成json
        dist_content = {}

        url_context = self.url_get()
        soup_replace = url_context.replace("<br />", "\n")
        soup = BeautifulSoup(soup_replace, 'html.parser')

        # 标题
        content_ = soup.find('h2', attrs={'class': 'content-header'}).string
        d1 = dist_content.setdefault("content_url", {})
        d1.update({"content-header": content_})

        title = soup.find_all('div', attrs={'class': 'entry-asset asset hentry'})

        for i_num in range(len(title)):
            # 获取每个id号
            div_id_ = title[i_num].get('id')
            d2 = d1.setdefault(div_id_, {})

            # 获取date
            ttlArea_date_ = soup.find_all('div', attrs={'class': 'ttlArea'})
            span_date_ = ttlArea_date_[i_num].find('span').get_text()
            d2.update({"date": span_date_})

            # 获取cat3 和 bookmark 内容
            cat3_content = soup.find_all('h2', attrs={'class': 'asset-name entry-title'})
            span_cat3 = cat3_content[i_num].find('span').get_text()
            a_bookmark = cat3_content[i_num].find('a').get_text()
            cat3_bookmark = span_cat3 + ' ' + a_bookmark
            d2.update({"entry-title": cat3_bookmark})

            # 获取entry_body_text的内容
            entry_body = soup.find_all('div', attrs={'class': 'entry-body'})
            entry_body_text = entry_body[i_num].find('div').get_text('\n', strip=True)
            entry_body_text_new = entry_body_text.replace(r"\n', '", '')
            d2.update({"content": entry_body_text_new})

        # 将dict转化成json格式
        json_content = json.dumps(dist_content)
        return json_content

    def data_handle(self, date_start, date_end):
        json_content = self.url_context_handle()

        con_ = json.loads(json_content)
        ll_date = jsonpath.jsonpath(con_, "$..date")

        # date_new = []

        # 正则匹配日期
        pattern = re.compile(r'(?P<year>[0-9]{4})年(?P<mouth>[0-9]+)月(?P<day>.?[0-9]+)日')
        for i_date in ll_date:
            result_search = re.search(pattern, i_date)
            result_tuple = result_search.groups()

            # 拼接成新的时间格式
            year_str = str(result_tuple[0]).strip()
            mouth_str = str(result_tuple[1]).strip().zfill(2)
            day_str = str(result_tuple[2]).strip().zfill(2)
            result_date = year_str + mouth_str + day_str

            # 时间转化
            time_array_ = time.strptime(result_date, "%Y%m%d")
            date_str = int(time.mktime(time_array_))

            # 本月份的时间，(x-1)月21号 ~ x月20号
            start_date = time.strptime(date_start, "%Y%m%d")
            end_date = time.strptime(date_end, "%Y%m%d")

            start_date_str = int(time.mktime(start_date))
            end_date_str = int(time.mktime(end_date))


            # result_date判断是否在本月内
            this_mouth_minus = end_date_str - start_date_str
            date_inner = date_str - start_date_str

            if date_inner >= 0:
                if this_mouth_minus - date_inner >= 0:
                    this_mouth_title = jsonpath.jsonpath(con_, expr='$..content-header')
                    this_mouth_date = jsonpath.jsonpath(con_, expr='$..date')
                    this_entry_title = jsonpath.jsonpath(con_, expr='$..entry-title')
                    this_mouth_context = jsonpath.jsonpath(con_, expr='$.content_url..content')

                    new_str = this_mouth_title[0] + '\n' + this_mouth_date[0] + '\n' + this_entry_title[0] + '\n' + this_mouth_context[0]
                    print(new_str)

if __name__ == '__main__':
    # 被趴的url地址
    url_root = ''

    # 输入本月开始时间
    date_this_mouth_start = input('Please enter the start date of the month in the format: 20200101: ')
    date_this_mouth_end = input('Please enter the end date of the month in the format: 20200131: ')

    con_res = nifty_information_get(url_root)
    con_res.data_handle(date_this_mouth_start, date_this_mouth_end)