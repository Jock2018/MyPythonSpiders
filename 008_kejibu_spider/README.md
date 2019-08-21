# 利用Python爬取中国科学技术部人类遗传资源管理7000+数据
## 一、需求
### 1. 目的
把中国科学技术部网站下，科技部门户 > 办事服务 > 行政许可	> 人类遗传资源管理 > 结果查询  [网址](http://www.most.gov.cn/bszn/new/rlyc/jgcx/)，里面所有的结果保存到一张Excel里面。如下图所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019080222182357.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI3MjgzNjE5,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/2019080222184685.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI3MjgzNjE5,size_16,color_FFFFFF,t_70)
### 2. 需求分析
总共有95个链接，共计93张表，其中有两个链接没有表格。
#### 方法一
直接打开一个新的Excel，一个一个链接去打开，然后复制、粘贴表格内容。
优点：简单粗暴、不用动脑，数据的准确性可靠
缺点：机械化操作、比较枯燥，而且遇到一些有换行符的表格，粘贴会分行，处理耗时巨大。
一开始我想着爬虫应该比较合适做这样的事，结果leader说爬虫同事说这个表格复制粘贴比较好，爬虫写起来会麻烦。我想数据量不算大，先按leader的建议，直接复制粘贴，等完成任务，回头再试试爬虫代码去爬，结果到了第20个，出现了换行符的情况，并且后面很多张表都是这样。这样每张表都要一行一行去重新复制、粘贴、删除，工作量将大大增加。所以只好先暂停，试试爬虫的处理方式。
#### 方法二
利用爬虫爬取。接下来主要就是讲解爬虫处理的思路。
## 二、爬虫实现
### 1. 整体思路
1. 拿到每张表格的网址
2. 依次爬取每张表格的网页
3. 解析爬取到的网页
4. 保存到Excel中
### 2. 抓取每张表格的网址
通过右击检查，如下图，href的值就是表格的网址。再查看一下源码，发现总共有115个这样的标签，而网页明明显示只有95个。这是因为它把第一页的20个表格重复了。所以95+20=115。所以后续抓取的时候，一定要注意抓取过的不能再抓。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190802221913270.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI3MjgzNjE5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190802221921174.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI3MjgzNjE5,size_16,color_FFFFFF,t_70)

因为这个国家官网没有什么反爬措施，所以requests+re直接搞定。因为比较简单，直接放出代码：
```py
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
```
这里稍微注意一下，我返回的是一个包含元组的列表。
### 3. 抓取每张表格的网页
抓取每张表格的网页，这个跟第一个基本一样，比较简单，直接用requests解决。
上代码:
```py
def get_html(self, goal_url):
    """
    请求包含表格内容的网页
    :param goal_url: 表格所在的网址
    :return:
    """
    response = requests.get(goal_url, headers=self.headers)
    return response.content
```
### 4. 解析爬取到的网页
因为要抓取的是表格内容，它的标签层级非常明显，所以我用lxml进行处理，然后xpath解析。
这里主要麻烦的地方在于，93张表格的格式不统一，所以解析的时候就需要用不同的解析方法，我要用四个解析函数，其中后面两个是单独为两张表写的，因为第一次爬，那两张表报错了。
这里稍微再介绍一下第四个方法。其他的表格都是一个tr标签是一行，但是`已批准的人类遗传资源行政许可项目信息汇总（2017年第十四批）`这张表的网页写的就不一样，表头用了两个tr标签，后面的一行数据用三个tr标签来写。所以就有了那一串的`if`，后面的数据是3个tr一个循环算一条记录。
### 5. 保存数据到Excel
保存数据这里我直接用的openpyxl。需要注意openpyxl会自动覆盖掉已有的Excel文件，相当于先删除，再写入，不是追加写入，所以一定要注意不要重名，避免数据被误删了。这个里面我还用了`set()`对于已爬取的链接进行判断，避免重复抓取。
### 6. 完整代码
最后我把上面的代码封装成了类进行调用，因为代码里面注释也比较清楚，所以不赘述了。
输出结果如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190802221943603.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI3MjgzNjE5,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190802221952825.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI3MjgzNjE5,size_16,color_FFFFFF,t_70)
看到数据乖乖到了Excel里面。出于对于数据的准确性，我把每张表的数据都对了一遍，避免数据不完整。
## 三、总结
这算是第一次用爬虫解决了工作上的任务。总结了下，爬虫在这里虽然好用，不过爬虫很可能抓取的数据不完整或者出错，所以在程序中一定要考虑充分数据的完整性，在关键的地方进行监测，输出信息，避免漏掉网页。拿到数据后，还要人工进行干预，校验。所以爬虫也是会花很大时间和精力的。具体的情况还是要具体分析，灵活选择解决方案。
