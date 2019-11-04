# -*- coding: utf-8 -*-
"""
    项目总体配置
    ~~~~~~~~~~~
    @copyright: 2018 by the nuctech training team
"""

import os
from datetime import timedelta


class Config(object):
    """基本"""

    DEBUG = False
    STATIC_URL = 'app/static'
    SECRET_KEY = 'c291cmNlLWRhdGEtbnVjdGVjaA==' # flask: source-data-nuctech'

    # -flask-jwt-extended: source-data-auth-nuctech
    JWT_SECRET_KEY = 'c291cmNlLWRhdGEtYXV0aC1udWN0ZWNo'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60*24*7)
    JWT_ERROR_MESSAGE_KEY = 'nuctech'

    # -七牛上传
    QINIU_DOMAIN_PREFIX = 'http://nathing.leeing.cn/'
    QINIU_ACCESS_KEY = os.environ.get(
        'QINIU_ACCESS_KEY', 'q6QLur7zYpyj9rUAeUwkKA3g2BxiGRugfevdqW7r')
    QINIU_SECRET_KEY = os.environ.get(
        'QINIU_SECRET_KEY', 'l8AfWuWW4DfK1TrZyPzUsXc8WKa_YojUgCUG040u')
    QINIU_BUCKET_NAME = 'nathing'

    # -db: mysql
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 是否开启跟踪; 开启的话，每次请求结束都会自动提交事务
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:123456!@#@10.15.225.23/SourceData'

    # -db: mongo
    MONGO_URI = 'mongodb://root:root123@10.15.225.23:27017/admin' # ^ sourceData 17端口
    MONGO_URI_IMAGEDATA = 'mongodb://10.15.225.10:27017/' # * 获取源数据CT/DR相关图像数据
    MONGO_URI_TRACKIO = 'mongodb://root:Train!ok.@10.15.225.23:27018/admin' # * sourceData项目<抖图数据库>. 18端口 : master-slave

    # -图像分发
    IMAGE_API_URL = 'https://devapi.anjianba.cn' # 配合图像分发的接口

    # -第三方登录
    SIGNALR_URL = 'https://stgws.anjianba.cn/api/plot/notice' # signalr连接地址
    LOGIN_THIRDPART_URL = 'https://stgapi.anjianba.cn/account/plot/login' # 第三方登录地址
    LOGIN_THIRDPART_VERSION = 2.4 # 第三方登录·接口版本号


class ProdConfig(Config):
    """生产"""

    MONGO_URI = 'mongodb://10.0.0.41:27017' # ^ sourceData:52.80.171.106

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Train!ok.@52.80.171.106/SourceData'


class TestConfig(Config):
    """测试"""

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:123456!@#@10.15.225.23/SourceData'


class DevConfig(Config):
    """开发"""

    DEBUG = True

    REDIS_URI = 'localhost'
    REDIS_PORT = 6379

    # MONGO_URI = 'mongodb://127.0.0.1:27017/sourcedata' # sourceData项目<本地测试>数据库

    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost/SourceData'
