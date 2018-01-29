#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
设置日志相关配置，输出实时的日志信息
"""
import os
import sys
import logging
import logging.handlers

from config.Global import BASE_PATH


class Logger(logging.Logger):
    def __init__(self):

        logger_name = "SecRss"
        level = logging.WARNING
        logger_file = BASE_PATH + logger_name + ".log"

        logging.Logger.__init__(self, logger_file)
        try:
            os.makedirs(os.path.dirname(logger_file))
        except Exception as reason:
            pass

        log_format = logging.Formatter(
            "[%(asctime)s] [" + logger_name + "] [%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s")

        if sys.stdout.isatty():
            try:
                ConsoleHandle = logging.StreamHandler()
                ConsoleHandle.setLevel(level)
                ConsoleHandle.setFormatter(log_format)
                self.addHandler(ConsoleHandle)
            except Exception as reason:
                self.error("%s" % reason)
        else:
            try:
                FileHandle = logging.FileHandler(logger_file)
                FileHandle.setLevel(level)
                FileHandle.setFormatter(log_format)
                self.addHandler(FileHandle)
            except Exception as reason:
                self.error("%s" % reason)

        try:
            handler = logging.handlers.RotatingFileHandler(
                filename=logger_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=1,
                mode='a',
                encoding="utf8",
                delay=0
            )
            handler.setFormatter(log_format)
        except Exception as reason:
            self.error("%s" % reason)
        else:
            self.addHandler(handler)


logger = Logger()
