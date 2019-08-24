"""TODO
后期可以连接一个IP代理池，这样就可以不用限速而且也有利于redis分布式爬取的部署
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*

import random
import requests
import logging
from useragent import agents  # 导入前面的useragent


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 建立一个filehandler来把日志记录在文件里，级别为error以上
file_handler = logging.FileHandler("logger_error.log", encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(file_handler)

def get_random_useragent():
    """
    获取随机User-Agent
    :return:
    """
    return random.choice(agents)

def get_proxy(proxy_type):
    """
    获取代理
    :param proxy_type: 代理类型，1=vps，2=random，3=foreign
    :return:
    """
    if proxy_type == 1:
        return {'http': '192.168.100.100:1234'}
    elif proxy_type == 2:
        return get_random_proxy()
    else:
        return {'http': '192.168.100.1000:1234'}

def get_random_proxy():
    url = 'http://192.168.100.100:1234/random'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': get_random_useragent(),
    }
    try:
        res = requests.get(url=url, timeout=5,headers=headers)
        if res.status_code == 200 and res.text:
            logger.info('当前代理IP=' + res.text)
            # print(res.text)  # 测试
            return {'http': res.text}
        else:
            return {'http': '192.168.100.100:1234'}

    except Exception as e:
        logger.error('===== get_proxy() 出错 ======' + str(e))
        return {'http': '192.168.100.100:1234'}

if __name__ == "__main__":
    for i in range(10):
        proxy = get_random_proxy()
        print(proxy)
