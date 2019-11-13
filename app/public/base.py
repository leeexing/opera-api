# -*- coding: utf-8 -*-
"""业务处理基础模块
   ~~~~~~~~~~~~~~~

    ：__author__ = 'nuctech'
    ：__date__ = '2018-11-23 14:55'
"""

from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt_claims

from app.db import MYSQL_DB, MONGO_DB
from app.util.logger import create_logger
from app.util.response import ResponseHelper
from app.public.argsparse import PAGING_PARSER


class BaseHandler:
    """请求处理基类"""

    def __init__(self, log_name='OPERA'):
        self.logger = create_logger(log_name)

    @property
    def db(self):
        """提供对数据库连接实例db的属性操作"""
        return MYSQL_DB

    @property
    def mongo(self):
        """获取 `sourceData` 数据库"""
        return MONGO_DB.cx['opera']

    @property
    def Response(self):
        """提供对帮助类Responsehelp的数据操作"""
        return ResponseHelper

    def get_paging_parser(self, default_limit=20):
        """获取相关的分页信息"""
        paging_args = PAGING_PARSER.parse_args()
        page = paging_args.get('page', 1)
        limit = paging_args.get('limit', default_limit)
        skip = (page - 1) * limit
        return skip, limit

    def parser_args(self):
        """获取get方法传递的参数"""
        return request.args

    def parser_form(self):
        """获取get/post方法的form表单参数"""
        return request.form

    def parser_files(self):
        """获取post方法传递的files文件"""
        return request.files

    def parser_json(self):
        """获取post方法传递的参数"""
        return request.get_json()

    def get_user(self):
        """获取当前用户信息"""
        return get_jwt_identity()

    def get_user_claims(self):
        """获取用户身份信息之外的信息"""
        return get_jwt_claims()
