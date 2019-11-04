# -*- coding: utf-8 -*-
"""日志模块"""

import os
import logging


def create_logger(name):
    """创建logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if not logger.handlers:
        # 控制台处理程序
        dhandler = logging.StreamHandler()
        dhandler.setFormatter(formatter)
        dhandler.setLevel(logging.DEBUG)
        logger.addHandler(dhandler)

        chandler = logging.FileHandler(os.path.join('./log/', 'info.log'), encoding='utf-8', delay='true')
        chandler.setFormatter(formatter)
        chandler.setLevel(logging.INFO)
        logger.addHandler(chandler)

        # 输入到文件
        fhandler = logging.FileHandler(os.path.join('./log/', 'error.log'), encoding='utf-8', delay='true')
        fhandler.setLevel(logging.ERROR)
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
    return logger
