#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
@author: Jock
"""

import requests
import re
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
    # 列表ls_page存储一页的电影信息
    ls_page = []
    # 构建获取排名的正则表达式
    reg_rank = re.compile('<em class="">(.+?)<', re.S)  # re.S'.'匹配换行
    ls_rank = reg_rank.finditer(data)
    # 构建获取影片名称的正则表达式
    reg_movie_name = re.compile('<img width="100" alt="(.+?)"', re.S)
    ls_movie_name = reg_movie_name.finditer(data)
    # 提取导演信息
    reg_movie_director = re.compile('导演:(.+?)&', re.S)
    ls_movie_director = reg_movie_director.finditer(data)
    # 获取年份
    reg_movie_year = re.compile('<br>(.+?)&', re.S)
    ls_movie_year = reg_movie_year.finditer(data)
    for i in range(25):
        # ls_item单独存储一部电影的信息,依次存储排名、电影名、导演名、年份
        ls_item = []
        ls_item.append(next(ls_rank).group(1)) # 添加排名
        ls_item.append(next(ls_movie_name).group(1))  # 添加电影名
        ls_item.append(next(ls_movie_director).group(1).split()[0]) # 添加导演名
        ls_item.append(next(ls_movie_year).group(1).split()[0]) # 添加年份
        ls_page.append(ls_item)
    return ls_page

# process_data(ls_page,fpath)输出、保存提取的信息
def process_data(ls_page, fpath):
    try:
        with open(fpath,'a', encoding='utf-8') as f: # 以可读可写的权限打开文件
            for i in ls_page:
                try:
                    s = ','.join(i) + '\n'
                    f.write(s) # 写入数据
                except:
                    continue
    except:
        # print("爬取失败") # 测试语句
        return ""

# 主函数
def main():
    fpath = r'C:\Users\admin\Desktop\豆瓣Top250电影.csv'
    i = 0
    while i < 250:
        url = 'https://movie.douban.com/top250?start=' + str(i)
        data = get_html_text(url)
        print(len(data))  # 测试用
        ls_page = extract_data(data)
        process_data(ls_page, fpath)
        i += 25

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


