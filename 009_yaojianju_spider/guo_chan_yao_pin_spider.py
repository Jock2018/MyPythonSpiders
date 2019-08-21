#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/8/5 23:00

@author: Jock
"""

import time
import logging
from collections import  deque
import requests
import pymysql
import hashlib


def get_total_pages(url):
    """
    获取总页数
    :param url:
    :return: total_pages
    """
    response = requests.get(url, timeout=2)
    total_pages = response.json()[0]['COUNT']
    return total_pages

def get_html(url):
    """
    请求网页
    :param url:
    :return: json数据
    """
    response = requests.get(url, timeout=2)
    return response.json()

def parse_content_html(data):
    """
    解析数据
    :param data:
    :return:
    """
    for each in data:
        yield ({ 'total_page': each['COUNT'], 'info': each['CONTENT'], 'id': each['ID']})

def parse_detail_html(data):
    """
    解析数据
    :param data:
    :return: dict
    """
    items = dict()
    for each in data:
        items[each['NAME']] = each['CONTENT'].strip()
    # del items['注']
    yield items

def get_md(url):
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    return m.hexdigest()

def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # 建立一个filehandler来把日志记录在文件里，级别为debug以上
    file_handler = logging.FileHandler("test.log", encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # 将相应的handler添加在logger对象中
    logger.addHandler(file_handler)
    return logger


def save_data(table, item):
    """
    存入数据库
    :param data:
    :return:
    """
    conn = pymysql.Connect(host="localhost", port=3306, user="root", password="your_password", db="drug", charset='utf8')
    cursor = conn.cursor()

    # keys = ', '.join(item.keys())
    keys = "`" + "`, `".join(item.keys()) + "`"
    values = ', '.join(['%s'] * len(item))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    sql = sql % tuple([r"'" + pymysql.escape_string(value) + r"'" if isinstance(value, str) else value
                       for value in item.values()])
    try:
        # sql = cursor.mogrify(sql)
        # print(sql)
        cursor.execute(sql)
        # cursor.execute(sql, value_tuple)
        conn.commit()
        print('插入{}表成功，数据内容：{}'.format(table, item))
        flag = True
    except Exception as e:
        print('插入{}表失败，失败代码{}数据内容：{}'.format(table, e, item))
        # logger.info('插入%s表中据失败，数据内容：%s', table, item)
        logger.error('插入%s表中据失败，数据内容：%s', table, item, exc_info=True)
        conn.rollback()  # 回滚
        flag = False
    finally:
        cursor.close()
        conn.close()
        return flag

def start_content_page(content_table, table_id):
    content_base_url = 'http://mobile.cfda.gov.cn/datasearch/QueryList?tableId={}&searchF=Quick%20Search&pageIndex={}&pageSize=15'
    detail_base_url = 'http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId={}&searchF=ID&searchK={}'
    # 获取目录页总页数
    print('开始获取目录页总条数')
    logger.info('开始获取目录页总条数')
    for i in range(1, 6):
        try:
            # +1保证取到最后一页
            total_pages = get_total_pages(content_base_url.format(table_id, i))  // 15 + 2
            break
        except Exception as e:
            if i == 5:
                logger.error('获取总页数失败', exc_info=True)
                print('程序提前结束！')
                print(e)
                return None
            continue
    # 设置抓取失败率为0.04
    fail_rate = 0.04
    # 设置尝试抓取次数，如果一个url抓取try_times次都失败，则放弃抓取
    try_times = 5
    # 计算总抓取次数,等比数列求和公式
    total_times = int((total_pages * (1-fail_rate**try_times)) / (1-fail_rate)) + 1
    # 测试
    # total_times = 1
    # total_pages = 2
    # 存入成功目录条数
    success_num = 0
    # 存入失败目录条数
    fail_num = 0
    # 构建双端队列存储详情页的url
    detail_url_dl = deque()
    # 构建一个目录页url的双端队列
    content_url_dl = deque([content_base_url.format(table_id, i) for i in range(1, total_pages)])
    print('开始抓取目录页...')
    logger.info('开始抓取目录页...')
    # 抓取目录页信息
    for i in range(total_times):
        if content_url_dl:
            content_url = content_url_dl.popleft()
            try:
                data = get_html(content_url)
                crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
                items = parse_content_html(data)
            except Exception:
                content_url_dl.append(content_url)
                continue
            # 写入数据到数据库
            for item in items:
                detail_url_dl.append(detail_base_url.format(table_id, item['id']))
                item['url'] = content_url
                item['crawl_time'] = crawl_time
                # print(item)
                flag = save_data(content_table, item)
                if flag:
                    success_num += 1
                else:
                    fail_num += 1
        if  not content_url_dl or (i == total_times-1):
            if content_url_dl:
                with open('fail_content_url.txt', 'w', encoding='utf-8') as f:
                    for content_url in content_url_dl:
                        f.write(content_url)
            fail_url_num = len(content_url_dl)
            print('累计成功抓取目录页{}条，失败{}条，写入目录页数据成功{}条，失败{}条'.format(total_pages-fail_url_num-1, fail_url_num, success_num,
                                                                 fail_num))
            logger.info('累计成功抓取目录页%s条，失败%s条，写入目录页数据成功%s条，失败%s条', total_pages-fail_url_num-1, fail_url_num, success_num,
                        fail_num)
            return detail_url_dl

def start_detail_page(detail_table, detail_url_dl):
    # 设置抓取失败率为0.04
    fail_rate = 0.04
    # 设置尝试抓取次数，如果一个url抓取try_times次都失败，则放弃抓取
    try_times = 5
    total_pages = len(detail_url_dl)
    # 计算总抓取次数,等比数列求和公式
    total_times = int((total_pages * (1-fail_rate**try_times)) / (1-fail_rate)) + 1
    # 存入成功详情页条数
    success_num = 0
    # 存入失败详情页条数
    fail_num = 0
    print('开始抓取详情页...')
    logger.info('开始抓取详情页...')
    # 抓取详情页信息
    for i in range(total_times):
        if detail_url_dl:
            detail_url = detail_url_dl.popleft()
            try:
                data = get_html(detail_url)
                crawl_time = time.strftime('%Y-%m-%d %X', time.localtime())
                items = parse_detail_html(data)
            except Exception:
                detail_url_dl.append(detail_url)
                continue
            # 写入数据到数据库
            for item in items:
                item['url'] = detail_url
                item['crawl_time'] = crawl_time
                # print(item)
                flag = save_data(detail_table, item)
                if flag:
                    success_num += 1
                else:
                    fail_num += 1

        if not detail_url or (i == total_times - 1):
            if detail_url_dl:
                with open('fail_detail_url.txt', 'w', encoding='utf-8') as f:
                    for detail_url in detail_url_dl:
                        f.write(detail_url)
            fail_url_num = len(detail_url_dl)
            print('累计成功抓取详情页{}条，失败{}条，写入详情页数据成功{}条，失败{}条'.format(total_pages-fail_url_num, fail_url_num, success_num, fail_num))
            logger.info('累计成功抓取详情页%s条，失败%s条，写入详情页数据成功%s条，失败%s条', total_pages-fail_url_num, fail_url_num, success_num, fail_num)
            return None

def main():
        content_table = 'zhi_ye_yao_shi_contents'
        detail_table = 'zhi_ye_yao_shi_detail'
        table_id = 122
        detail_url_dl = start_content_page(content_table, table_id)
        # for i in detail_url_dl:
        #     print(i)
        start_detail_page(detail_table, detail_url_dl)
        # with open('zhiye.txt', 'w', encoding='utf-8') as f:
        #     for each in detail_url_dl:
        #         f.write(each)

if __name__ == '__main__':
    logger = logger()
    main()

