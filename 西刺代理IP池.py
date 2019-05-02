#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jock
"""

import requests
import traceback
import re
import time

class GetIP():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def get_html(self, url):
        print('正在下载页面：{}'.format(url))
        try:
            r = requests.get(url, headers=self.headers)  # 爬取完整的网页数据
            r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
            return r.text  # 以字符串的形式返回爬取的网页内容
        except Exception:
            print('下载页面出错：{}'.format(url))
            traceback.print_exc()

    def get_ip_list(self, url):
        data = self.get_html(url)
        pat_1 = re.compile(r'/></td>(.*?)</tr>', re.S)  # 构建、编译第一层正则表达式,匹配一个IP完整信息块
        pat_2 = re.compile(r'<td>(.*?)</td>', re.S)  # 构建、编译第二层正则表达式，提取完整的IP信息
        iter_ip = pat_1.finditer(data)  # 找到所有IP信息块，返回生成器
        list_ip = []  # 存放IP
        # 遍历iter_ip，提取并存入IP
        for i in iter_ip:
            try:
                key = pat_2.findall(i.group())
                list_ip.append(key[3].lower() + '://' + key[0] + ':' + key[1])
            except:
                print('解析IP地址出错')
                traceback.print_exc()
                continue
        return list_ip


def main():
    url = 'https://www.xicidaili.com/'
    ip = GetIP()
    list_ip = ip.get_ip_list(url)
    for i in list_ip:
        print(i)
        time.sleep(0.1)

if __name__ == '__main__':
    main()