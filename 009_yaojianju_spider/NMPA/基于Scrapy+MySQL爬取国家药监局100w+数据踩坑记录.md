{"国产药品": 25, "进口药品":36,"国产器械": 26, "进口器械": 27, "国产特殊用途化妆品":68, "进口特殊用途化妆品":69, "职业药师": 122, "网上药店": 96}
## 1. 网页请求返回json数据的处理
Scrapy的返回对象Response没有json()方法，所以如果请求结果是json数据的话,必须用json.loads()方法处理成python可以处理的json对象。即
```py
result = json.loads(response.text)
```
## 2. Scrapy的Request中回调函数间的信息交流
Scrapy中Request的回调函数间的信息交流是scrapy 1.7之前的版本是通过meta参数传递实现，最新的scrapy 1.7开始推荐是用cb_kwargs进行传递，无法通过return返回。比如start_requests(self)方法中有：total_pages = yield Request(url, callback=self.get_total_pages),尽管在get_total_pages(self, response)方法中有return total pages, 但是返回到start_requests(self)方法中的total_pages是None，而不是get_total_pages()返回的total_pages。示例：
```py
# 错误的方法
    def start_requests(self):
        """
        发起初始请求
        :return: 
        """
        url = 'http://mobile.cfda.gov.cn/datasearch/QueryList?tableId=36&searchF=Quick%20Search&pageIndex=1&pageSize=15'
        total_pages = yield Request(url, callback=self.get_total_pages)
        print(total_pages)

    def get_total_pages(self, response):
        """
        获取目录页总页数
        :param url:
        :return: total_pages
        """
        # 要用json.loads()将字符串转换为json数据
        total_items = json.loads(response.text)[0]['COUNT'] # 获取总条数
        # 获取总页数,每页15条数据,所以页数=总条数/15，如果巧好整除则+1,否则+2
        if total_items/15 == int(total_items/15):
            total_pages = int(total_items/15) + 1
        else:
            total_pages = int(total_items/15) + 2
        return total_pages

# 推荐的方法
   def start_requests(self):
        """
        发起初始请求
        :return:
        """
        # 1.数据库实例初始化
        self.mysql = MysqlClient(self.settings)
        table_id = 25
        page_index = 1
        logger.info('开始发起请求...')
        content_url = self.content_base_url.format(table_id=table_id, page_index=page_index)
        # Request跟进我们的URL,并将response作为参数传递给self.get_total_pages,典型的回调函数
        yield Request(content_url, callback=self.get_total_pages, cb_kwargs=dict(table_id=table_id))

    def get_total_pages(self, response, table_id):
        """
        获取目录页总页数
        :param url:
        :return: total_pages
        """
        # 要用json.loads()将字符串转换为json数据
        total_items = json.loads(response.text)[0]['COUNT'] # 获取总条数
        # print(total_items)
        # 获取总页数,每页15条数据,所以页数=总条数/15，如果巧好整除则+1,否则+2
        if total_items/15 == int(total_items/15):
            total_pages = int(total_items/15) + 1
        else:
            total_pages = int(total_items/15) + 2
        # table_id = response.meta['table_id'] # 这是原来meta的用法,现在已经不推荐这么传参数
        count = 0
        for page_index in range(1, total_pages):
            count += 1
            content_url = self.content_base_url.format(table_id=table_id, page_index=page_index)
            if count > 50:
                count = 0
                # time.sleep(random.uniform(1, 2)) # 请求延迟
            # 请求产品的目录页
            yield Request(url=content_url, callback=self.parse_content, cb_kwargs=dict(table_id=table_id))
```
## 3. MySQL报错：pymysql.err.InternalError: (1046, '')
这个问题花了很多时间，总结一下解决的思路和流程。
### 3.1 打印一下sql语句，同时放入Navicat中执行。
打印sql语句的方法:
```py
print('开始执行sql语句')
sql = self.cursor.mogrify(sql)
print(sql)
```
如果Navicat中执行成功，则说明sql语句没有问题，问题出在连接数据库上面。转入步骤2。
如果Navicat中执行失败，说明sql语句有问题，检查表的名字、字段名是否意义对应，以及其中是否包含特殊字符，有特殊字符的表名或者字段名需要用”``“包裹，比如有“/”。中文的建议用”\`字段名\`“或者"\`表名\`".
### 3.2 检查程序连接mysql的设置是否正确，打印出配置信息检查：
```py
print('开始连接MySQL数据库')
print('打印主机号:{}'.format(self.host))
print(self.user)
print(self.password)
print(self.db)
print(self.charset)
print(self.port)
```
## 4. pymysql报错：AttributeError: 'NoneType' object has no attribute 'encoding' using pymysql
原因是：charset编码问题，pymysql世界里，“utf8”是一个有效的字符集，但“utf-8”不是。具体参考：https://stackoverflow.com/questions/49828342/attributeerror-nonetype-object-has-no-attribute-encoding-using-pymysql
```py
self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                        port=self.port,charset=self.charset)
# self.charset不能是'utf-8',可以是'utf8'
```
## 5. Navicat中利用sql建表
一个非常好用的测试sql语法的网站:[sql测试](http://sqlfiddle.com/#!9/bb3b91)
### 5.1 基本信息表
这个表通用，只要把表名替换一下就可以了。
```sql
-- 进口药品基本表
DROP TABLE IF EXISTS `jkyp_content_info`;
CREATE TABLE `jkyp_content_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
 `product_count` INT(11) DEFAULT NULL,
  `product_info` VARCHAR(255) DEFAULT NULL,
  `product_id` INT(11) DEFAULT NULL,
  `url` VARCHAR(255) DEFAULT NULL,
  `crawl_time` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```
### 5.2 详细信息表
详细表每个都需要单独建一个表和scrapy.Field()字段比较麻烦。
不过这里我写了个小脚本帮助来偷点懒。
```py
s = """批准文号
产品名称
...
原批准文号
药品本位码
药品本位码备注
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

```
屏幕会自动输出符合格式的scrapy.Field()和建表部分，直接复制粘贴完善一些就好。省事很多。

```sql
-- 国产药品详细信息
DROP TABLE IF EXISTS `gcyp_detail_info`;
CREATE TABLE `gcyp_detail_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
 `product_id` INT(11) DEFAULT NULL,
 `批准文号` VARCHAR(255) DEFAULT NULL,
 `产品名称` VARCHAR(255) DEFAULT NULL,
 `英文名称` VARCHAR(255) DEFAULT NULL,
 `商品名` VARCHAR(255) DEFAULT NULL,
 `剂型` VARCHAR(255) DEFAULT NULL,
 `规格` VARCHAR(255) DEFAULT NULL,
 `上市许可持有人` VARCHAR(255) DEFAULT NULL,
 `生产单位` VARCHAR(255) DEFAULT NULL,
 `生产地址` VARCHAR(255) DEFAULT NULL,
 `产品类别` VARCHAR(255) DEFAULT NULL,
 `批准日期` VARCHAR(255) DEFAULT NULL,
 `原批准文号` VARCHAR(255) DEFAULT NULL,
 `药品本位码` VARCHAR(255) DEFAULT NULL,
 `药品本位码备注` VARCHAR(255) DEFAULT NULL,
 `注` VARCHAR(255) DEFAULT NULL,
  `url` VARCHAR(255) DEFAULT NULL,
  `crawl_time` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```
## 6. IP被封问题
参考文献：[Scrapy研究探索（七）——如何防止被ban之策略大集合](https://blog.csdn.net/u012150179/article/details/35774323)
### 6.1 策略一：设置download_delay
download_delay的作用主要是设置下载的等待时间，大规模集中的访问对服务器的影响最大，相当与短时间中增大服务器负载。
下载等待时间长，不能满足段时间大规模抓取的要求，太短则大大增加了被ban的几率。
使用注意：
download_delay可以设置在settings.py中，也可以在spider中设置。
### 6.2  策略二：禁止cookies
所谓cookies，是指某些网站为了辨别用户身份而储存在用户本地终端（Client Side）上的数据（通常经过加密），禁止cookies也就防止了可能使用cookies识别爬虫轨迹的网站得逞。
使用：
在settings.py中设置COOKIES_ENABLES=False。也就是不启用cookies middleware，不想web server发送cookies。
### 6.3 策略三：使用user-agent池
所谓的user-agent，是指包含浏览器信息、操作系统信息等的一个字符串，也称之为一种特殊的网络协议。服务器通过它判断当前访问对象是浏览器、邮件客户端还是网络爬虫。在request.headers可以查看user agent。
scrapy本身是使用Scrapy/版本号 来表明自己身份的。这也就暴露了自己是爬虫的信息
### 6.4 策略四：使用IP池
web server应对爬虫的策略之一就是直接将你的IP或者是整个IP段都封掉禁止访问，这时候，当IP封掉后，转换到其他的IP继续访问即可。
可以使用Scrapy+Tor+polipo
配置方法与使用教程可参见：http://pkmishra.github.io/blog/2013/03/18/how-to-run-scrapy-with-TOR-and-multiple-browser-agents-part-1-mac/。
### 6.5 策略五：分布式爬取
这个，内容就更多了，针对scrapy，也有相关的针对分布式爬取的GitHub repo。可以搜一下。
## 7. 保存至MySQL数据库去重问题
使用sql语句，添加去重函数：
```py
    def _select_product_id(self, query_sql=''):
        """
        去重函数,查找product_id字段,如果存在返回[(1,1)],不存在则会返回()
        :param query_sql:
        :return:
        """
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("set names utf8") # utf8 字符集
        self.cursor.execute(query_sql)
        # sql = self.cursor.mogrify(query_sql)
        # print(sql)
        # print(self.cursor.fetchall())
        return self.cursor.fetchall() # cursor.fetchall()只能调用一次，再次调用就返回()空元组

    def _insert(self, insert_sql=''):
        """
       执行插入MySQL
        :param insert_sql:
        :return:
        """
        try:
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute("set names utf8") # utf8 字符集
            # insert_sql = self.cursor.mogrify(insert_sql)
            # print(insert_sql)
            self.cursor.execute(insert_sql)
            self.conn.commit()
            return True
        except Exception as e:
            logger.error('err:s% : %s', insert_sql, str(e))
            self.conn.rollback()
            self.cursor.close()
            return False

    def save_base_info(self, item):
        """
        保存信息到MySQL数据库
        :param item:
        :return:
        """
        try:
            table = item.table
            product_id = item['product_id']
            # keys = ', '.join(item.keys())
            keys = '`' + '`, `'.join(item.keys()) + '`' # 因为是item类名称有中文
            values = ', '.join(['%s'] * len(item))
            insert_sql = f'INSERT INTO `{table}`({keys}) VALUES ({values})'
            insert_sql = insert_sql % tuple([r"'" + pymysql.escape_string(value) + r"'" if isinstance(value, str) else value
                               for value in item.values()])
            # query_sql = f'SELECT EXISTS (SELECT 1 FROM `{table}` WHERE product_id={product_id})'
            query_sql = f'SELECT 1 FROM `{table}` WHERE product_id={product_id}'
            if self._select_product_id(query_sql):
                logger.info(f'{product_id}已存在MySQL数据库中')
                return True
            else:
                return self._insert(insert_sql)

        except Exception as e:
            logger.error('保存信息失败，item=%s, err=%s', item, str(e))
            return None
```
## 8. 解决scrapy自动进行网页去重问题
参考链接[Scrapy - Filtered duplicate request](https://stackoverflow.com/questions/39730566/scrapy-filtered-duplicate-request)
因为在获取目录页总页数时，访问过一次page_index=1的url，是scrapy有基于布隆过滤器对url进行去重，导致后面存储时，这个网址无法再次抓取。
## 8.1 解决办法一：在Request中加入参数：dont_filter = True
这种办法需要在每一个Request加入dont_filter=True参数。
```py
yield Request(content_url, callback=self.get_total_pages, cb_kwargs=dict(table_id=table_id), dont_filter = True)
```
## 8.2 解决办法二：配置setting
可以一步到位，不用一个个去设置Request。
```py
# settings.py
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
```
## 9 利用字典避免多重if...elif..else提升效率
因为涉及到很多个table_id，如果用if...elif...else...需要写的特别长，而且效率会受影响。如下：
```py
        if table_id == 36:
            item = JKYPDetailItem()
        elif table_id == 25:
            item = GCYPDetailItem()
        elif table_id == 26:
            item = GCQXDetailItem()
        elif table_id == 27:
            item = JKQXDetailItem()
        elif table_id == 68:
            item = GCTSYTHZPDetailItem()
        elif table_id == 69:
            item = JKTSYTHZPDetailItem()
        elif table_id == 122:
            item = ZYYSDetailItem()
        elif table_id == 96:
            item = WSYDDetailItem()
        else:
            logger.error('表格号有误,请确认输入表格号是否正确！')
            return None
        print(item.table)
```
采用字典优化后
```py
 # 采用字典, 避免过多的if...elif...else,提升效率,简化代码
        detail_items = {36:JKYPDetailItem(), 25:GCYPDetailItem(), 26:GCQXDetailItem(), 27: JKQXDetailItem(),
                        68: GCTSYTHZPDetailItem(), 69: JKTSYTHZPDetailItem(), 122: ZYYSDetailItem(),
                        96: WSYDDetailItem()
                        }
        item = detail_items.get(table_id)
        if not item:
            logger.error('表格号有误,请确认输入表格号是否正确！')
```
代码量减少了，而且执行也会变快。
## 10. pymysql.err.DataError: (1406, '')
因为数据量大于了设置的数据类型。对于文本类型，超过了varchar(255)，则需要设置为LONGTEXT类型， 把表的字段类型修改即可。
## 11 Todo
1. 日志的配置不够灵活，后期需要优化。
2. 构建一个IP池，不再设置下载延迟，提升效率。
