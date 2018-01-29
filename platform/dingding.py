# -*- coding:utf-8 -*-
# Author: sky
# Email:  sky@03sec.com
import json
import datetime
import requests

from platform.Base import Base
from utils.logger import logger


class Platform(Base):
    def __init__(self, news_list):
        super(Platform, self).__init__(news_list)
        self.info = {
            "name": "dingding",
            "status": True,
            "save": True,
            "images": True,
            "webhook": "https://oapi.dingtalk.com/robot/send?access_token=x"
        }

    def insert_feed_card(self):
        """
        添加feedCard
        :return:
        """
        result = {
            "feedCard": {
                "links": []
            },
            "msgtype": "feedCard"
        }

        first_msg = {
            "title": "【{today}】今日安全聚合".format(
                today=str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(
                    datetime.date.today().day)),
            "messageURL": "http://www.03sec.com",
            "picURL": "http://mweb.03sec.com/2018-01-15-sec.png"
        }
        result['feedCard']['links'].append(first_msg)
        return result

    def transform(self):
        """
        对传入的采集列表转换为dingding平台接口允许的格式
        :return:
        """
        result = self.insert_feed_card()

        for item in self.news_list:
            for news in item['target']:
                push_news = {'picUlr': "", 'title': news['title'], 'messageURL': news['link']}
                result['feedCard']['links'].append(push_news)
        return result

    def push_message(self):
        """
        推送消息
        :return Boolean:
        """
        result = self.transform()

        headers = {
            "Content-Type": "application/json"
        }
        r = requests.post(self.info['webhook'], headers=headers, data=json.dumps(result)).json()

        if r['errcode'] is not 0:
            logger.warn("消息发送失败：【" + json.dumps(result) + "】")
            return False
        else:
            return True
