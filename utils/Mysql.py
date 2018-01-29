# -*- coding:utf-8 -*-
# Author: sky
# Email:  sky@03sec.com

from config.Global import get_config
import pymysql

from utils.logger import logger


class Mysql:
    def __init__(self):
        self.db_host = get_config("database", "db_host")
        self.db_user = get_config("database", "db_user")
        self.db_pass = get_config("database", "db_pass")
        self.db_name = get_config("database", "db_name")
        self.db = pymysql.connect(self.db_host, self.db_user, self.db_pass, self.db_name,charset='utf8')
        self.cursor = self.db.cursor()
        self.cursor.execute("SET NAMES utf8")
        self.db.commit()
    def save_to_post(self, title, source_url, s_from, content, published_time, m_hash):
        save_to_post = """INSERT INTO `sys_posts` ( `sys_posts`.title, `sys_posts`.source_url, `sys_posts`.from, `sys_posts`.content, `sys_posts`.published_time, `sys_posts`.hash )VALUES( %s,%s,%s,%s,%s,%s )"""
        try:
            # 执行sql语句
            self.cursor.execute(save_to_post,(title, source_url, s_from, content,published_time,m_hash))
            # 执行sql语句
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            logger.warn('Mysql Insert Error:save_to_post' + str(e))

    def save_to_collect(self, published_time, m_hash, m_count):
        save_to_collect = """INSERT INTO `sys_collect_count` (  published_time, hash,count )VALUES('{published_time}' , '{m_hash}','{m_count}' )"""
        try:
            # 执行sql语句
            self.cursor.execute(save_to_collect.format(published_time=published_time, m_hash=m_hash, m_count=m_count))
            # 执行sql语句
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            self.db.rollback()
            logger.warn('Mysql Insert Error:save_to_collect' + str(e))

    def close_db(self):
        self.db.close()

    def query(self):
        pass


if __name__ == '__main__':
    pass
