# -*- coding:utf-8 -*-
# Author: sky
# Email:  sky@03sec.com
from dateutil import parser
import json
import requests
import feedparser
from config.Global import BASE_PATH, load_platform
from utils.logger import logger
import time


class Core:
    def __init__(self):
        self.news_list = []

    def get_rss_title_and_url(self):
        """
        根据规则获取rss的标题和url
        :return:
        """
        try:
            rss_data = json.load(open(BASE_PATH + "/core/data.json", "r", encoding="utf-8"))
            for item in rss_data:
                rss = feedparser.parse(requests.get(item['rss']).content)['entries']
                push_new_list = {"source": item, "target": []}

                for it in rss:
                    datetime_struct = parser.parse(it['published'])
                    published = datetime_struct.strftime("%Y-%m-%d")

                    today = time.strftime("%Y-%m-%d")

                    if today == published:
                        if item['has_content'] in it['title']:
                            push_new_list["target"].append(it)
                self.news_list.append(push_new_list)
        except Exception as e:
            logger.warn("获取RSS标题和URL异常:" + str(e))

    def send_message(self):
        for platform_name in load_platform():
            load_platform()[platform_name].Platform(self.news_list).run()

    @staticmethod
    def sec_news_run():
        sec_core = Core()
        sec_core.get_rss_title_and_url()
        return sec_core.send_message()


if __name__ == '__main__':
    print(Core.sec_news_run())
