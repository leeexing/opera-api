# -*- coding: utf-8 -*-
"""数据库连接器模块"""

import pika
from pymongo import MongoClient
from redis import StrictRedis, ConnectionPool

from app.conf.config import Config, DevConfig

mongo_client_trackio = None
mongo_client_imagedata = None


def get_redis_connection():
    """redis连接器"""
    return StrictRedis(host=DevConfig.REDIS_URI, port=DevConfig.REDIS_PORT, charset='utf-8', decode_responses=True)


def get_mongo_imagedata_connection():
    """Mongodb连接器<maindatabase>"""
    global mongo_client_imagedata

    if not mongo_client_imagedata:
        mongo_client_imagedata = MongoClient(host=Config.MONGO_URI_IMAGEDATA)
        return mongo_client_imagedata
    return mongo_client_imagedata


def get_mongo_trackio_connection():
    """Mongodb连接器<trackiodata:restfulapi>"""
    global mongo_client_trackio

    if not mongo_client_trackio:
        mongo_client_trackio = MongoClient(host=Config.MONGO_URI_TRACKIO)
        return mongo_client_trackio
    return mongo_client_trackio


def get_rabbitmq_connection():
    """Rabbitmq消息队列连接"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return connection


class RedisConnect:
    """redis连接器
        : 线程池方式连接，不同服务之间连接功能同一个线程
    """
    pool = None

    def __init__(self):
        if not RedisConnect.pool:
            RedisConnect.pool = ConnectionPool(host=DevConfig.REDIS_URI, port=DevConfig.REDIS_PORT, db=0, decode_responses=True)
        self.r_connect = StrictRedis(connection_pool=RedisConnect.pool)

    def set_hash_data(self, name, key, value):
        """设置hash"""
        return self.r_connect.hset(name, key, value)
