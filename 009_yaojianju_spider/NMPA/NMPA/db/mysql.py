#!/usr/bin/env python
# -*- coding: utf-8 -*
import pymysql
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 建立一个filehandler来把日志记录在文件里，级别为error以上
file_handler = logging.FileHandler("mysql_error.log", encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(file_handler)

class MysqlClient(object):

    def __init__(self, settings):
        """
        初始化连接MySQL的参数
        :param settings: 参数字典
        """
        self.settings = settings
        self.host = self.settings.get('MYSQL_HOST')
        self.user = self.settings.get('MYSQL_USER')
        self.password = self.settings.get('MYSQL_PASSWORD')
        self.port = self.settings.get('MYSQL_PORT')
        self.db = self.settings.get('MYSQL_DATABASE')
        self.charset = self.settings.get('MYSQL_CHARSET')
        self.conn = None
        self.cursor = None
        self._conn()

    def _conn(self):
        """连接MySQL数据库"""
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user,  password=self.password, db=self.db,
                                        port=self.port,charset=self.charset)
            logger.info('MySQL数据库连接成功')
            return True
        except Exception as e:
            logger.info('MySQL数据库连接失败, 失败原因：%s', str(e))
            return False

    def _select_product_id(self, query_sql=''):
        """
        去重函数,查找product_id字段,如果存在返回[{'1': 1}],不存在则会返回()
        :param query_sql:
        :return:
        """
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("set names utf8")  # utf8 字符集
        self.cursor.execute(query_sql)
        # sql = self.cursor.mogrify(query_sql)
        # print(sql)
        # print(self.cursor.fetchall())
        return self.cursor.fetchall()  # cursor.fetchall()只能调用一次，再次调用就返回()空元组

    def _insert(self, insert_sql=''):
        """
       执行插入MySQL
        :param insert_sql:
        :return:
        """
        try:
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute("set names utf8")  # utf8 字符集
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
            keys = '`' + '`, `'.join(item.keys()) + '`'  # 因为是item类名称有中文
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

    def save_base_infos(self, items):
        """
        保存信息到MySQL数据库,适用于多条items
        :param items:
        :return
        """
        for item in items:
            if not self.save_base_info(item):
                logger.error('保存信息失败，item=%s', str(item))
                return False

        return True

    def close(self):
        """
        关闭mysql连接
        :return:
        """
        self.conn.close()
