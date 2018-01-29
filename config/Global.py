# -*- coding:utf-8 -*-
# Author: sky
# Email:  sky@03sec.com
import os
from configparser import ConfigParser
from functools import partial

from pluginbase import PluginBase

BASE_PATH = partial(os.path.join, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))('')


def get_config(section, key):
    """
    获取配置信息
    :param section:
    :param key:
    :return:
    """
    config = ConfigParser()
    path = BASE_PATH + "config/news.cfg"
    config.read(path)
    return config.get(section, key)


def load_platform():
    """
    载入信息发布平台
    :return:
    """
    platform_dir = BASE_PATH + 'platform'

    platform_base = PluginBase(
        package=str('platform').replace('/', '.'), searchpath=[platform_dir]
    )
    platform_source = platform_base.make_plugin_source(
        searchpath=[platform_dir], persist=True
    )
    platform_dict = {}
    for platform_name in platform_source.list_plugins():
        __tmp = platform_source.load_plugin(platform_name)
        if hasattr(__tmp, 'Platform') and hasattr(__tmp, 'Base'):
            if platform_source.load_plugin(platform_name).Platform([]).info['status']:
                platform_dict[platform_name] = platform_source.load_plugin(platform_name)

    return platform_dict
