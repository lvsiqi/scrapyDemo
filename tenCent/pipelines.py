# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import pymysql

from tenCent import settings

'''
class TencentPipeline(object):
    def open_spider(self, spider):
        """
         # spider (Spider 对象) – 被开启的spider
         # 可选实现，当spider被开启时，这个方法被调用。
        :param spider:
        :return:
        """
        self.file = open('tencent.json', 'w', encoding='utf-8')
        json_header = '{ "tencent_info":['
        self.count = 0
        self.file.write(json_header)  # 保存到文件

    def close_spider(self, spider):
        """
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        :param spider:
        :return:
        """
        json_tail = '] }'
        self.file.seek(self.file.tell() - 1)  # 定位到最后一个逗号
        self.file.truncate()  # 截断后面的字符
        self.file.write(json_tail)  # 添加终止符保存到文件
        self.file.close()

    def process_item(self, item, spider):
        """
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。

        :param item:
        :param spider:
        :return:
        """

        content = json.dumps(dict(item), ensure_ascii=False, indent=2) + ","  # 字典转换json字符串
        self.count += 1
        print('content', self.count)
        self.file.write(content)  # 保存到文件

'''


class DBPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
            # 插入数据
            self.cursor.execute(
                """insert into jobs(position_name, position_link, position_number ,publish_times, position_duty ,position_require ,position_type)
                value (%s, %s, %s, %s, %s, %s, %s)""",
                (item['position_name'],
                 item['position_link'],
                 item['position_number'],
                 item['publish_times'],
                 item['position_duty'],
                 item['position_require'],
                 item['position_type']
                 ))

            # 提交sql语句
            self.connect.commit()
            return
