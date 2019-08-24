

【国产药品表目录页】
http://mobile.cfda.gov.cn/datasearch/QueryList?tableId=25&searchF=Quick%20Search&pageIndex=1&pageSize=15
构造 url = 'http://mobile.cfda.gov.cn/datasearch/QueryList?tableId=25&searchF=Quick%20Search&pageIndex={}&pageSize=15'
i range(1, 11024)
【进口药品表目录页
http://mobile.cfda.gov.cn/datasearch/QueryList?tableId=36&searchF=Quick%20Search&pageIndex=1&pageSize=15
range(1. 273)
【国产特殊用途化妆品目录页】
http://mobile.cfda.gov.cn/datasearch/QueryList?tableId=68&searchF=Quick%20Search&pageIndex=1&pageSize=15

【国产药品表详情页】
http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=25&searchF=ID&searchK={}
构造 url = 'http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=25&searchF=ID&searchK={}'
i range(1, 166565),比165339多出来1225条数据
【进口药品表详情页】
http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=36&searchF=ID&searchK={}
range(1, 2768)
4075条数据
【国产特殊用途化妆品详情页】
http://mobile.cfda.gov.cn/datasearch/QueryRecord?tableId=68&searchF=ID&searchK={}
数据41504条

【表的编号】
国产药品表：25
进口药品表：36
国产特殊用途化妆品：68
进口化妆品：69
执业药师注册人员：122
网上药店：96


【项目思路参考链接】
https://my.oschina.net/hengbao666/blog/1551645
https://blog.csdn.net/qq_39138295/article/details/83348551
https://www.zhihu.com/question/54817892

【charles】
[charles简明教程](https://www.cnblogs.com/xiaocainiao920/p/8667949.html)


【mysql数据库保存参考】
https://blog.csdn.net/weixin_44239541/article/details/89766158
https://blog.csdn.net/qq_36019490/article/details/88773946
https://www.cnblogs.com/woider/p/5926744.html
[Mysql数据库迁移：善用Navicat工具，事半功倍](https://blog.csdn.net/wd2014610/article/details/81487004)

【logging】
https://cuiqingcai.com/6080.html
[Python3 使用 logging 模块输出日志中的中文乱码解决办法](https://blog.csdn.net/HeatDeath/article/details/79094093)

【hashlib】
[scrapy中用hashlib.md5 处理 url](https://www.jianshu.com/p/271b20f7574f)
# -*- coding:utf-8 -*-
import hashlib

def get_md(url):
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print (get_md(("http://jobbole.com").encode("utf-8")))

guo_chan_yao_pin_biao_detail

爬取时间：
item['crawl_time'] = time.strftime('%Y-%m-%d %X', time.localtime())


【后续思考】
组件的构建：
logger  db   helper spider  布隆过滤器
性能的思考：
多线程、多进程、协程
redis分布式爬取
去重策略
定时爬取

构建一个失败url池，后面继续爬10次，如果都失败，说明不行

再构建一个写入文件，专门存储失败的网址信息分开：目录页（url），和详情页网址（id数字）