#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jock
"""


import time
import random
import json
import logging
import scrapy
from scrapy.http import  Request  # 一个单独的request的模块,需要跟进URL的时候，需要用它
from NMPA.items import JKYPBaseItem, JKYPDetailItem, GCYPBaseItem, GCYPDetailItem, GCQXBaseItem, GCQXDetailItem
from NMPA.items import JKQXBaseItem, JKQXDetailItem, GCTSYTHZPBaseItem, GCTSYTHZPDetailItem, JKTSYTHZPBaseItem
from NMPA.items import JKTSYTHZPDetailItem, ZYYSBaseItem, ZYYSDetailItem, WSYDBaseItem, WSYDDetailItem
from NMPA.db.mysql import MysqlClient


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 建立一个filehandler来把日志记录在文件里，级别为error以上
file_handler = logging.FileHandler("error.log", encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(file_handler)
# StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class MySpider(scrapy.Spider):

    name = 'NMPA'  # 整个项目，这个名字必须唯一
    allowed_domains = ['mobile.cfda.gov.cn']  # 非必须,在使用爬取规则时需要，它的作用是只会跟进allowed_domains中的URL，不存在的会忽略
    content_base_url = 'http://mobile.cfda.gov.cn/datasearch/QueryList?tableId={table_id}&searchF=Quick%20Search&pageIndex={page_index}&pageSize=15'
    detail_base_url = 'http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId={table_id}&searchF=ID&searchK={product_id}'

    def start_requests(self):
        """
        发起初始请求
        :return:
        """
        # 1.数据库实例初始化
        self.mysql = MysqlClient(self.settings)
        # [25, 36, 26, 27, 68, 69,122, 96]
        table_id = 25
        page_index = 1
        logger.info('开始发起请求...')
        content_url = self.content_base_url.format(table_id=table_id, page_index=page_index)
        # Request跟进我们的URL,并将response作为参数传递给self.get_total_pages,典型的回调函数
        yield Request(content_url, callback=self.get_total_pages, cb_kwargs=dict(table_id=table_id), dont_filter = True)  # callback=不写也可以
        """yield Request,请求新的URL,后面跟的是回调函数,你需要哪一个函数来处理这个返回值,就调用哪个函数,
                    返回值response会以参数的形式传递给你所调用的函数, cb_kwargs是scrpay 1.7最新的用法,可以实现
                    向回调函数传参的作用, dont_filter = True指的是不对这个url进行过滤处理
                    """

    def get_total_pages(self, response, table_id):
        """
        获取目录页总页数,并构建目录页URL,发起请求
        :param url:
        :return: total_pages
        """
        # 要用json.loads()将字符串转换为json数据
        total_items = json.loads(response.text)[0]['COUNT']  # 获取总条数
        # print(total_items)
        # 获取总页数,每页15条数据,所以页数=总条数/15，如果巧好整除则+1,否则+2
        if total_items/15 == int(total_items/15):
            total_pages = int(total_items/15) + 1
        else:
            total_pages = int(total_items/15) + 2
        # table_id = response.meta['table_id']  # 这是原来meta的用法,现在已经不推荐这么传参数
        count = 0
        print(total_pages)
        for page_index in range(1, total_pages):
            count += 1
            content_url = self.content_base_url.format(table_id=table_id, page_index=page_index)
            if count > 100:
                count = 0
                time.sleep(random.uniform(0.2, 1))  # 请求延迟
            # 请求产品的目录页
            yield Request(url=content_url, callback=self.parse_content, cb_kwargs=dict(table_id=table_id),
                          dont_filter = True)
            # yield Request(url=content_url, callback=self.parse_detail, meta={'table_id': table_id})

    def parse_content(self, response, table_id):
        """
        解析目录页,并构建详情页URL,发起请求
        :param response:
        :param table_id:
        :return:
        """
        results = json.loads(response.text)
        # logger.info('打印目录页数据')
        # print(results)  # 调试用
        # 采用字典, 避免过多的if...elif...else,提升效率,简化代码
        detail_items = {36: JKYPBaseItem(), 25: GCYPBaseItem(), 26: GCQXBaseItem(), 27: JKQXBaseItem(),
                        68: GCTSYTHZPBaseItem(), 69: JKTSYTHZPBaseItem(), 122: ZYYSBaseItem(),
                        96: WSYDBaseItem()
                        }
        item = detail_items.get(table_id)
        # print(type(item))
        # 判断输入表格号是否在字典中, 因为scrapy自带的Item返回为{},所以不能用not item来判断
        if item == None:
            logger.error('表格号有误,请确认输入表格号是否正确！')
            return None
        for result in results:
            # print(item.table)
            item['product_count'] = result['COUNT']  # 字典的取值方式
            item['product_info'] = result['CONTENT']
            item['product_id'] = result['ID']
            item['url'] = response.url  # 获取网页的url
            item['crawl_time'] = time.strftime('%Y-%m-%d %X', time.localtime())  # 获取爬取时间
            product_id = result['ID']
            detail_url = self.detail_base_url.format(table_id=table_id,product_id=product_id )
            print(list(item.values()))
            # print(detail_url)
            # time.sleep(random.uniform(1, 3))  # 请求延迟
            # 请求产品的详情页
            yield Request(url=detail_url, callback=self.parse_detail,
                          cb_kwargs=dict(table_id=table_id, product_id=product_id), dont_filter = True)
            # print('回调完成')
            if not self.mysql.save_base_info(item=item):  # 保存到mysql数据库
                logger.error('保存目录页信息失败！item=%s', item)

    def parse_detail(self, response, table_id, product_id):
        """
        解析详情页
        :param response:
        :param table_id:
        :param product_id:
        :return:
        """
        results = json.loads(response.text)
        # print(results)
        # 采用字典, 避免过多的if...elif...else,提升效率,简化代码
        detail_items = {36: JKYPDetailItem(), 25:GCYPDetailItem(), 26:GCQXDetailItem(), 27: JKQXDetailItem(),
                        68: GCTSYTHZPDetailItem(), 69: JKTSYTHZPDetailItem(), 122: ZYYSDetailItem(),
                        96: WSYDDetailItem()
                        }
        item = detail_items.get(table_id)
        if item == None:
            logger.error('表格号有误,请确认输入表格号是否正确！')
            return None
        # print(item.table)
        for result in results:
             item[str(result['NAME'].replace('（', '_').replace('）', '').replace(' ', '').replace('/', '_')
                      .replace('、', '_'))] = result['CONTENT'].strip().replace('\t', ' ')
             # print(str(result['NAME'].replace('（', '_').replace('）', '').replace(' ', '').replace('/', '_').replace('、', '_')))  # 方便建表测试用的,勿删！！！
        item['product_id'] = product_id
        item['url'] = response.url  # 获取网页的url
        item['crawl_time'] = time.strftime('%Y-%m-%d %X', time.localtime())  # 获取爬取时间
        del item['注']
        print(list(item))
        if not self.mysql.save_base_info(item=item):  # 保存到mysql数据库
            logger.error('保存详情页信息失败！item=%s', item)

    def parse(self, response):
        """
        start_resquests和Requests返回response的默认处理函数
        :param response:
        :return:
        """
        pass

