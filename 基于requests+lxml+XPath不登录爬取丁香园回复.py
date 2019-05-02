#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/4/9 13:41

@author: Jock
"""


import requests
from lxml import etree
import time

# get_html_text(url)获取网页信息
def get_html_text(url):
    try:
        r = requests.get(url)  # 爬取完整的网页数据
        r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
        return r.text  # 以字符串的形式返回爬取的网页内容
    except:
        print("访问出错")
        return ""  # 发生异常，返回空字符串

# extract_data(data)提取网页内容
def extract_data(data):
    # 做好ElementTree
    tree = etree.HTML(data)
    # 列表ls_ms回复信息
    ls_ms = []
    # 以列表形式，返回所有包含所需信息的td标签
    ls = tree.xpath('//td[@class="postbody"]')
    n = len(ls)
    for i in range(n):
        try:
            ls_ms.append('\n'.join(ls[i].xpath('.//text()')).strip())  # 把每个td标签中的信息放入列表中
        except:
            print('出错')
            continue
    return ls_ms

# 主函数
def main():
    url = 'http://www.dxy.cn/bbs/thread/626626#626626'
    data = get_html_text(url)
    ls_ms = extract_data(data)
    n = len(ls_ms)
    print('【问题】：' + ls_ms[0])
    for i in range(1,n):
        print('【回复'+ str(i) + '】是：', end='')
        print(ls_ms[i])

# 测试时间
def count_spend_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    time_dif = (end_time - start_time)
    second = time_dif%60
    minute = (time_dif//60)%60
    hour = (time_dif//60)//60
    print('spend ' + str(hour) + 'hours,' + str(minute) + 'minutes,' + str(second) + 'seconds')

if __name__ == '__main__':
    count_spend_time(main)