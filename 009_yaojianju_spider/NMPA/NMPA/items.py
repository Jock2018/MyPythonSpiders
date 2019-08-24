#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GCYPBaseItem(scrapy.Item):
    """国产药品库基本目录信息,table_id=25"""
    table = 'gcyp_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class GCYPDetailItem(scrapy.Item):
    """国产药品库详细信息,table_id=25"""
    table = 'gcyp_detail_info'

    product_id = scrapy.Field()
    批准文号 = scrapy.Field()
    产品名称 = scrapy.Field()
    英文名称 = scrapy.Field()
    商品名 = scrapy.Field()
    剂型 = scrapy.Field()
    规格 = scrapy.Field()
    上市许可持有人 = scrapy.Field()
    生产单位 = scrapy.Field()
    生产地址 = scrapy.Field()
    产品类别 = scrapy.Field()
    批准日期 = scrapy.Field()
    原批准文号 = scrapy.Field()
    药品本位码 = scrapy.Field()
    药品本位码备注 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class JKYPBaseItem(scrapy.Item):
    """进口药品库基本目录信息,table_id=36"""
    table = 'jkyp_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class JKYPDetailItem(scrapy.Item):
    """进口药品库详细信息,table_id=36"""
    table = 'jkyp_detail_info'

    product_id = scrapy.Field()
    注册证号 = scrapy.Field()
    原注册证号 = scrapy.Field()
    注册证号备注 = scrapy.Field()
    分包装批准文号 = scrapy.Field()
    公司名称_中文 = scrapy.Field()
    公司名称_英文 = scrapy.Field()
    地址_中文 = scrapy.Field()
    地址_英文 = scrapy.Field()
    国家_地区_中文 = scrapy.Field()
    国家_地区_英文 = scrapy.Field()
    产品名称_中文 = scrapy.Field()
    产品名称_英文 = scrapy.Field()
    商品名_中文 = scrapy.Field()
    商品名_英文 = scrapy.Field()
    剂型_中文 = scrapy.Field()
    规格_中文 = scrapy.Field()
    包装规格_中文 = scrapy.Field()
    生产厂商_中文 = scrapy.Field()
    生产厂商_英文 = scrapy.Field()
    厂商地址_中文 = scrapy.Field()
    厂商地址_英文 = scrapy.Field()
    厂商国家_地区_中文 = scrapy.Field()
    厂商国家_地区_英文 = scrapy.Field()
    发证日期 = scrapy.Field()
    有效期截止日 = scrapy.Field()
    分包装企业名称 = scrapy.Field()
    分包装企业地址 = scrapy.Field()
    分包装文号批准日期 = scrapy.Field()
    分包装文号有效期截止日 = scrapy.Field()
    产品类别 = scrapy.Field()
    药品本位码 = scrapy.Field()
    药品本位码备注 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class GCQXBaseItem(scrapy.Item):
    """国产器械库基本目录信息,table_id=26"""
    table = 'gcqx_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class GCQXDetailItem(scrapy.Item):
    """国产器械库详细信息,table_id=26"""
    table = 'gcqx_detail_info'

    product_id = scrapy.Field()
    注册证编号 = scrapy.Field()
    注册人名称 = scrapy.Field()
    注册人住所 = scrapy.Field()
    生产地址 = scrapy.Field()
    代理人名称 = scrapy.Field()
    代理人住所 = scrapy.Field()
    产品名称 = scrapy.Field()
    型号_规格 = scrapy.Field()
    结构及组成 = scrapy.Field()
    适用范围 = scrapy.Field()
    其他内容 = scrapy.Field()
    备注 = scrapy.Field()
    批准日期 = scrapy.Field()
    有效期至 = scrapy.Field()
    附件 = scrapy.Field()
    产品标准 = scrapy.Field()
    变更日期 = scrapy.Field()
    邮编 = scrapy.Field()
    主要组成成分_体外诊断试剂 = scrapy.Field()
    预期用途_体外诊断试剂 = scrapy.Field()
    产品储存条件及有效期_体外诊断试剂 = scrapy.Field()
    审批部门 = scrapy.Field()
    变更情况 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class JKQXBaseItem(scrapy.Item):
    """进口器械库基本目录信息,table_id=27"""
    table = 'jkqx_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class JKQXDetailItem(scrapy.Item):
    """进口器械库详细信息,table_id=27"""
    table = 'jkqx_detail_info'

    product_id = scrapy.Field()
    产品名称 = scrapy.Field()
    注册证编号 = scrapy.Field()
    注册人名称 = scrapy.Field()
    注册人住所 = scrapy.Field()
    生产地址 = scrapy.Field()
    代理人名称 = scrapy.Field()
    代理人住所 = scrapy.Field()
    型号_规格 = scrapy.Field()
    结构及组成 = scrapy.Field()
    适用范围 = scrapy.Field()
    生产国或地区_英文 = scrapy.Field()
    附件 = scrapy.Field()
    其他内容 = scrapy.Field()
    备注 = scrapy.Field()
    批准日期 = scrapy.Field()
    有效期至 = scrapy.Field()
    生产厂商名称_中文 = scrapy.Field()
    产品名称_中文 = scrapy.Field()
    产品标准 = scrapy.Field()
    生产国或地区_中文 = scrapy.Field()
    售后服务机构 = scrapy.Field()
    变更日期 = scrapy.Field()
    主要组成成分_体外诊断试剂 = scrapy.Field()
    预期用途_体外诊断试剂 = scrapy.Field()
    产品储存条件及有效期_体外诊断试剂 = scrapy.Field()
    审批部门 = scrapy.Field()
    变更情况 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class GCTSYTHZPBaseItem(scrapy.Item):
    """国产特殊用途化妆品库基本目录信息,table_id=68"""
    table = 'gctsythzp_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class GCTSYTHZPDetailItem(scrapy.Item):
    """国产特殊用途化妆品库详细信息,table_id=68"""
    table = 'gctsythzp_detail_info'

    product_id = scrapy.Field()
    产品名称 = scrapy.Field()
    产品类别 = scrapy.Field()
    生产企业 = scrapy.Field()
    生产企业地址 = scrapy.Field()
    批准文号 = scrapy.Field()
    批件状态 = scrapy.Field()
    批准日期 = scrapy.Field()
    批件有效期 = scrapy.Field()
    卫生许可证号 = scrapy.Field()
    产品名称备注 = scrapy.Field()
    备注 = scrapy.Field()
    产品技术要求 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()





class JKTSYTHZPBaseItem(scrapy.Item):
    """进口特殊用途化妆品库基本目录信息,table_id=69"""
    table = 'jktsythzp_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class JKTSYTHZPDetailItem(scrapy.Item):
    """进口特殊用途化妆品库详细信息,table_id=69"""
    table = 'jktsythzp_detail_info'

    product_id = scrapy.Field()
    产品名称_中文 = scrapy.Field()
    批件状态 = scrapy.Field()
    产品名称_英文 = scrapy.Field()
    产品类别 = scrapy.Field()
    生产国_地区 = scrapy.Field()
    生产企业_中文 = scrapy.Field()
    生产企业_英文 = scrapy.Field()
    生产企业地址 = scrapy.Field()
    在华申报责任单位 = scrapy.Field()
    在华责任单位地址 = scrapy.Field()
    批准文号 = scrapy.Field()
    批准日期 = scrapy.Field()
    批件有效期 = scrapy.Field()
    备注 = scrapy.Field()
    产品名称备注 = scrapy.Field()
    产品技术要求 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class ZYYSBaseItem(scrapy.Item):
    """执业药师库基本目录信息,table_id=122"""
    table = 'zyys_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class ZYYSDetailItem(scrapy.Item):
    """执业药师库详细信息,table_id=122"""
    table = 'zyys_detail_info'

    product_id = scrapy.Field()
    姓名 = scrapy.Field()
    注册证编号 = scrapy.Field()
    执业地区 = scrapy.Field()
    执业类别 = scrapy.Field()
    执业范围 = scrapy.Field()
    执业单位 = scrapy.Field()
    有效期 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class WSYDBaseItem(scrapy.Item):
    """网上药店库基本目录信息,table_id=96"""
    table = 'wsyd_content_info'

    product_count = scrapy.Field()
    product_info = scrapy.Field()
    product_id = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


class WSYDDetailItem(scrapy.Item):
    """网上药店库详细信息,table_id=96"""
    table = 'wsyd_detail_info'

    product_id = scrapy.Field()
    证书编号 = scrapy.Field()
    服务范围 = scrapy.Field()
    单位名称 = scrapy.Field()
    法定代表人 = scrapy.Field()
    单位地址 = scrapy.Field()
    省份 = scrapy.Field()
    网站名称 = scrapy.Field()
    IP地址 = scrapy.Field()
    域名 = scrapy.Field()
    发证日期 = scrapy.Field()
    有效截至日期 = scrapy.Field()
    邮编 = scrapy.Field()
    注 = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()


"""
{"国产药品": 25, "进口药品":36,"国产器械": 26, "进口器械": 27,
 "国产特殊用途化妆品":68, "进口特殊用途化妆品":69, "职业药师": 122,
 "网上药店": 96}
 """



# class JKYPDetailItem(scrapy.Item):
#     """进口药品库详细信息英文字段版"""
#     table = 'jkyp_detail_info'
#
#     registration_number = scrapy.Field()
#     original_registration_number = scrapy.Field()
#     original_registration_number_note = scrapy.Field()
#     sub_package_approval_number = scrapy.Field()
#     company_name_zh = scrapy.Field()
#     company_name_en = scrapy.Field()
#     address_zh = scrapy.Field()
#     address_en = scrapy.Field()
#     country_region_zh = scrapy.Field()
#     country_region_en = scrapy.Field()
#     product_name_zh = scrapy.Field()
#     product_name_en = scrapy.Field()
#     commercial_name_zh = scrapy.Field()
#     commercial_name_en = scrapy.Field()
#     formulation_zh = scrapy.Field()
#     specification_zh = scrapy.Field()
#     packing_specification = scrapy.Field()
#     manufacturer_zh = scrapy.Field()
#     manufacturer_en = scrapy.Field()
#     vendor_address_zh = scrapy.Field()
#     vendor_address_en = scrapy.Field()
#     manufacturer_country_region_zh = scrapy.Field()
#     manufacturer_country_region_en = scrapy.Field()
#     date_of_issue = scrapy.Field()
#     expiration_date = scrapy.Field()
#     sub_package_company_name = scrapy.Field()
#     sub_packaged_company_address = scrapy.Field()
#     sub_package_number_approval_date = scrapy.Field()
#     sub_package_number_expiration_date = scrapy.Field()
#     product_category = scrapy.Field()
#     drug_standard_code = scrapy.Field()
#     drug_standard_code_note = scrapy.Field()
#     note = scrapy.Field()
#     url = scrapy.Field()
#     crawl_time = scrapy.Field()

