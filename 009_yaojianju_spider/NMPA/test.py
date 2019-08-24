#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/8/21 9:00

@author: Jock
"""
# import json
# import requests
#
# def get_html(url):
#     """
#     请求网页
#     :param url:
#     :return: json数据
#     """
#     response = requests.get(url, timeout=2)
#     return response.json()
#
# url = 'http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=36&searchF=ID&searchK=2553'
#
# data = requests.get(url).text
# result = json.loads(data)
# print(result)
# print(result.get('d'))


s = """证书编号
服务范围
单位名称
法定代表人
单位地址
省份
网站名称
IP地址
域名
发证日期
有效截至日期
邮编
注
"""

s = s.split('\n') # 转换成列表
ls_1 = list()
ls_2 = list()
# 建表用
for each in s[:-1]:
    ls_1.append('`' + each + '`' + ' VARCHAR(255) DEFAULT NULL,')
for each in ls_1:
    print(each)

print('='*100)
# 建scrapy.Field()用
ls_2.append('product_id = scrapy.Field()')
for each in s[:-1]:
    ls_2.append(each + ' = scrapy.Field()')
ls_2.extend(['url = scrapy.Field()', 'crawl_time = scrapy.Field()'])
for each in ls_2:
    print(each)



