# -*- coding:utf-8 -*-
# Author: sky
# Email:  sky@03sec.com
import hashlib
import re
import uuid
import datetime
import os
import requests
import time
from bs4 import BeautifulSoup

from config.Global import BASE_PATH, get_config
from utils.Mysql import Mysql
from utils.logger import logger


class Base(object):
    def __init__(self, news_list):
        self.news_list = news_list  # 获取到的新闻列表
        self.info = {
            "name": "xx",  # 平台名字，需要与文件名一致
            "status": False,  # 平台是否启用
            "save": True,  # 是否存入数据库
            "images": True  # 是否下载图片
        }

        hash = hashlib.md5()
        hash.update(bytes(str(datetime.datetime.today()), encoding='utf-8'))
        self.m_hash = hash.hexdigest()
        self.count = 0
        self.picBlacklist = str(get_config('picBlacklist', 'urls')).split(',')
        self.static_domain = get_config("server", "static_url")
        if os.path.exists(BASE_PATH + "/static") is not True:
            os.mkdir(BASE_PATH + "/static")

    def push_message(self):
        """
        该平台的发送消息的实现方法，必须重写
        :return:
        """
        pass

    def save_post_to_mysql(self, title, source_url, s_from, published_time, start_str, end_str, lazyLoading, lazyLabel):
        """
        保存文章到数据库
        :param title:
        :param source_url:
        :param s_from:
        :param published_time:
        :param start_str:
        :param end_str:
        :param lazyLoading:
        :param lazyLabel:
        :return:
        """
        content = ''
        try:
            r = requests.get(source_url).text
            content = r[r.find(start_str):r.find(end_str)]
            if lazyLoading:
                content = content.replace(lazyLabel, "src")
            if self.info['images']:
                content = self.download_image(content)
        except Exception as e:
            r = requests.get(source_url).text
            content = r[r.find(start_str):r.find(end_str)]
            logger.warn("下载图片出错：" + str(e))
        finally:
            try:
                Mysql().save_to_post(title=title, source_url=source_url, s_from=s_from, content=content,
                                     published_time=published_time, m_hash=self.m_hash)
            except Exception as e:
                logger.warn("保存文章到数据库出错,错误信息" + str(e))

    def download_image(self, content):
        """
        下载图片
        :param content:
        :return:
        """
        bs = BeautifulSoup(content, 'lxml')
        images = bs.find_all("img")
        for image in images:
            tmpUrl = image.get('src')
            (url, suffix) = re.findall(r'(.+?\.(png|jpg|gif|jpeg))', tmpUrl)[0]
            try:
                if url not in self.picBlacklist:
                    ir = requests.get(url)
                    if ir.status_code == 200:
                        logger.info("获取到图片{picUlr}".format(picUlr=url))
                        filename = str(uuid.uuid1()) + "." + suffix

                        open(BASE_PATH + 'static/' + filename, 'wb').write(ir.content)

                        logger.info("下载图片{picName},本地图片名字{localPicName}"
                                    .format(picName=url, localPicName=filename))
                        content.replace(url, self.static_domain + filename)
            except Exception as e:
                logger.warn("下载图片异常:" + str(e))
        return content

    def save_count_to_mysql(self, published_time, m_count):
        """
        保存今日采集数量
        :param published_time:
        :param m_count:
        :return:
        """
        try:
            Mysql().save_to_collect(published_time=published_time, m_hash=self.m_hash, m_count=m_count)
        except Exception as e:
            logger.warn("保存今日采集数量到数据库出错，错误信息" + str(e))

    def run(self):
        """
        启动方法
        :return Boolean:
        """
        try:
            if self.push_message():
                logger.info("消息推送成功！")
                if self.info['save']:
                    today = published = time.strftime("%Y-%m-%d")
                    for item in self.news_list:
                        for target in item['target']:
                            self.save_post_to_mysql(target['title'], target['link'], item['source']['s_title'],
                                                    published,
                                                    item['source']['start_str'], item['source']['end_str'],
                                                    item['source']['lazyLoading'], item['source']['lazyLabel'])
                            self.count += 1
                    self.save_count_to_mysql(today, self.count)
                    logger.info("保存日期 %s 的文章成功！")
        except Exception as e:
            logger.warn("推送平台异常，异常信息为:" + str(e))
