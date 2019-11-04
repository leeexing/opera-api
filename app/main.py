# -*- coding: utf-8 -*-
"""APP主模块"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.conf.config import DevConfig, ProdConfig, TestConfig

from app.api import api
from app.util.jwt_auth import BindJwt
from app.db import MYSQL_DB as db, MONGO_DB as mongo


def create_app(env='DEV'):
    """创建app"""
    app = Flask('OPERA_API', static_folder=DevConfig.STATIC_URL)
    if env == 'DEV':
        CORS(app)        # 跨域支持
        app.config.from_object(DevConfig)
    elif env == 'PROD':
        app.config.from_object(ProdConfig)
    elif env == 'TEST':
        app.config.from_object(TestConfig)

    jwt = JWTManager(app)
    BindJwt.init(jwt)    # 初始化jwt-auth

    db.init_app(app)     # 初始化MYSQL数据库
    mongo.init_app(app)  # 初始化MONGO数据库
    api.init_app(app)    # 绑定restful api
    return app
