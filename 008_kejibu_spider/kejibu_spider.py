#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/8/1 13:37

@author: Jock
"""


import re
import requests
from lxml import etree
import openpyxl
import time


class YiChuanSpider(object):
    def __init__(self):
        """
        初始化: 起始url,base_url, headers
        :return:
        """
        self.start_url = 'http://www.most.gov.cn/bszn/new/rlyc/jgcx'
        self.base_url = 'http://www.most.gov.cn/bszn/new/rlyc/jgcx/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    def get_url_name_list(self):
        """
        获取每张表的url和name
        :return: [(url, name), ..., (url, name)]
        """
        response = requests.get(self.start_url, headers=self.headers)
        # print(response.status_code)
        # 网页是'gb2312'编码
        content = response.content.decode("gb2312")
        # 正则进行匹配
        pattern = re.compile(r'<a target="_blank" href=".(.*?)" >(.*?)</a>')
        # findall 返回一个list,元素是一个元组(url, name)，用finditer返回一个迭代器
        url_name_list = pattern.findall(content)
        return url_name_list

    def get_html(self, goal_url):
        """
        请求包含表格内容的网页
        :param goal_url: 表格所在的网址
        :return:
        """
        response = requests.get(goal_url, headers=self.headers)
        return response.content

    def parse_html_1(self, data):
        """
        解析网页，提取表格内容，用于解析最新的表格格式
        :param data:
        :return:
        """
        tree = etree.HTML(data)
        table = tree.xpath('//tbody/tr')
        # table为None，说明网页中不存在表格，不解析
        if not table:
            raise ValueError("网页中没有表格")
        for each in table:
            row  = each.xpath('./td')
            column_1 = row[0].xpath('./p//text()')[0]
            column_2 = ''.join(row[1].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            column_3 = ''.join(row[2].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            column_4 = ''.join(row[3].xpath('./p//text()'))
            column_5 = ''.join(row[4].xpath('./p//text()'))
            column_6 = ''.join(row[5].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            column_7 = ''.join(row[6].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            yield [str(column_1), str(column_2) , str(column_3), str(column_4), str(column_5),str(column_6), str(column_7)]
            # print([column_1, column_2 , column_3, column_4, column_5,column_6, column_7])

    def parse_html_2(self, data):
        """
        解析网页，提取表格内容，用于解析旧的表格格式
        :param data:
        :return:
        """
        tree = etree.HTML(data)
        table = tree.xpath('//tbody/tr')
        if not table:
            raise ValueError("网页中没有表格")
        for each in table:
            # xpath进行解析，然后结合join()方法replace()方法对数据进行简单清洗
            row  = each.xpath('./td')
            column_1 = row[0].xpath('./p//text()')[0]
            column_2 = ''.join(row[1].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            column_3 = ''.join(row[2].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            column_4 = ''.join(row[3].xpath('./p//text()'))
            column_5 = ''.join(row[4].xpath('./p//text()'))
            column_6 = ''.join(row[5].xpath('./p//text()')).replace('\n', '').replace(' ', '')
            yield [str(column_1), str(column_2), str(column_3), str(column_4), str(column_5), str(column_6)]
            # print([column_1, column_2 , column_3, column_4, column_5,column_6])

    def parse_html_3(self, data):
        """
        解析网页，提取表格内容，专门提取2017年第十五批
        :param data:
        :return:
        """
        tree = etree.HTML(data)
        table = tree.xpath('//tbody/tr')
        # table为None，说明网页中不存在表格，不解析
        if not table:
            raise ValueError("网页中没有表格")
        for each in table:
            row = each.xpath('./td')
            column_1 = row[0].xpath('.//text()')[0]
            column_2 = ''.join(row[1].xpath('.//text()')).replace('\n', '').replace(' ', '')
            column_3 = ''.join(row[2].xpath('.//text()')).replace('\n', '').replace(' ', '')
            column_4 = ''.join(row[3].xpath('.//text()'))
            column_5 = ''.join(row[4].xpath('.//text()'))
            column_6 = ''.join(row[5].xpath('.//text()')).replace('\n', '').replace(' ', '')
            column_7 = ''.join(row[6].xpath('.//text()')).replace('\n', '').replace(' ', '')
            yield [str(column_1), str(column_2) , str(column_3), str(column_4), str(column_5),str(column_6), str(column_7)]
            # print([column_1, column_2 , column_3, column_4, column_5,column_6, column_7])

    def parse_html_4(self, data):
        """
        解析网页，提取表格内容,专门提取2017年第十四批，这个比较麻烦
        column_2被拆分为到了3个tr里面，所以除了第1,2个tr标签外，剩下的tr标签是3个一循环
        :param data:
        :return:
        """
        tree = etree.HTML(data)
        table = tree.xpath('//tbody/tr')
        # table为None，说明网页中不存在表格，不解析
        if not table:
            raise ValueError("网页中没有表格")
        # flag用来记录循环，相当于一个哨兵
        flag = 0
        for each in table:
            flag += 1
            row = each.xpath('./td')
            if flag == 1:
                column_1 = row[0].xpath('.//text()')[0]
                column_2 = ''.join(row[1].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_3 = ''.join(row[2].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_4 = ''.join(row[3].xpath('.//text()'))
                column_5 = ''.join(row[4].xpath('.//text()'))
                column_6 = ''.join(row[5].xpath('.//text()')).replace('\n', '').replace(' ', '').replace(' ', '')
                column_7 = ''.join(row[6].xpath('.//text()')).replace('\n', '').replace(' ', '')
                continue
            if flag == 2:
                column_2_2 = row[0].xpath('.//text()')[0]
                column_2 = column_2 + column_2_2
                yield [str(column_1), str(column_2), str(column_3), str(column_4), str(column_5), str(column_6),
                       str(column_7)]
                # print([column_1, column_2 , column_3, column_4, column_5,column_6, column_7])
                continue
            if flag % 3 == 0:
                column_1 = row[0].xpath('.//text()')[0]
                column_2 = ''.join(row[1].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_3 = ''.join(row[2].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_4 = ''.join(row[3].xpath('.//text()'))
                column_5 = ''.join(row[4].xpath('.//text()'))
                column_6 = ''.join(row[5].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_7 = ''.join(row[6].xpath('.//text()')).replace('\n', '').replace(' ', '')
                continue
            if flag % 3 == 1:
                column_2_1 = ''.join(row[0].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_2 = column_2 + column_2_1
                continue
            if flag % 3 == 2:
                column_2_2 = ''.join(row[0].xpath('.//text()')).replace('\n', '').replace(' ', '')
                column_2 = column_2 + column_2_2
                yield [str(column_1), str(column_2), str(column_3), str(column_4), str(column_5), str(column_6),
                       str(column_7)]
                # print([column_1, column_2 , column_3, column_4, column_5,column_6, column_7])

    def save(self):
        """
        保存数据为CSV
        :return:
        """
        # 创建excel
        xls = openpyxl.Workbook()
        # 激活sheet
        sheet = xls.active
        url_name_list = self.get_url_name_list()
        # 记录抓取的网址数
        url_count = 0
        # 记录抓取的数据条数，不计算表头
        total_item = 0
        # 存储已经爬取的url，避免重复爬取
        crawl_url_set = set()
        # 记录失败的url和name
        fail_url_name_list = list()
        for item in url_name_list:
            goal_url = 'http://www.most.gov.cn/bszn/new/rlyc/jgcx/{}'.format(item[0])
            # 不爬取爬过的网页
            if goal_url not in crawl_url_set:
                crawl_url_set.add(goal_url)
                url_count += 1
                # print("开始抓取第{}个URL：{},批次是：{}".format(url_count, goal_url, item[1]))
                data = self.get_html(goal_url)
                try:
                    rows = self.parse_html_1(data)
                    for row in rows:
                        # 把每一行写入excel
                        sheet.append(row)
                        total_item += 1
                    print("抓取第{}个URL：{}，成功".format(url_count, goal_url))
                    # print(result)
                except:
                    try:
                        rows = self.parse_html_2(data)
                        for row in rows:
                            # 把每一行写入excel
                            sheet.append(row)
                            total_item += 1
                        print("抓取第{}个URL：{},成功".format(url_count, goal_url))
                    except:
                        try:
                            rows = self.parse_html_3(data)
                            for row in rows:
                                # 把每一行写入excel
                                sheet.append(row)
                                total_item += 1
                            print("抓取第{}个URL：{},成功".format(url_count, goal_url))
                        except:
                            try:
                                rows = self.parse_html_4(data)
                                for row in rows:
                                    # 把每一行写入excel
                                    sheet.append(row)
                                    total_item += 1
                                print("抓取第{}个URL：{},成功".format(url_count, goal_url))
                            except:
                                print("抓取第{}个URL：{}，失败!!!!".format(url_count, goal_url))
                                fail_url_name_list.append((goal_url,item[1]))
                                continue
        print("累计抓取{}条数据".format(total_item - (url_count-len(fail_url_name_list))))
        # 关闭Excel
        xls.save('all_1.xlsx')
        print("抓取成功{}个url，失败{}个url，失败的url和批次如下：".format(url_count-len(fail_url_name_list), len(fail_url_name_list)))
        for each in fail_url_name_list:
            print("网址：{},批次：{}".format(each[0], each[1]))

if __name__ == '__main__':
    start_time = time.perf_counter()
    spider = YiChuanSpider()
    spider.save()
    end_time = time.perf_counter()
    print('累计用时：{}s'.format(end_time - start_time))
    """
    # 测试用例
    # 测试spider.get_url_name_list()
    url_name_list = spider.get_url_name_list()
    for each in url_name_list:
        print(each)
    # 测试spider.get_html(url)，spider.parse_html_1(data)
    url_1 = 'http://www.most.gov.cn/bszn/new/rlyc/jgcx/201907/t20190709_147573.htm'
    data_1 = spider.get_html(url_1)
    print(data_1)
    result = spider.parse_html_1(data_1)
    for i in result:
        print(i)
    # 测试spider.get_html(url)，spider.parse_html_2(data)
    url_2 = 'http://www.most.gov.cn/bszn/new/rlyc/jgcx//201507/t20150703_120511.htm'
    data_2 = spider.get_html(url_2)
    result = spider.parse_html_2(data_2)
    for i in result:
        print(i)
    """



