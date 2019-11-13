# -*- coding: utf-8 -*-
"""运维数据"""

from collections import Counter
from bson.objectid import ObjectId

import jieba
from flask_restplus import marshal

from app.public.base import BaseHandler
from app.public.fields import operation_field


class OperationManager(BaseHandler):

    def fetch_operaion_list(self):
        """获取运维数据列表"""
        try:
            skip, limit = self.get_paging_parser()
            count = self.mongo.operation.count()
            operations = list(self.mongo.operation.find().skip(skip).limit(limit))
            data = {
                'operations': marshal(operations, operation_field),
                'total': count
            }
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def fetch_operaion_detail(self, operation_id):
        """获取运维数据具体那周的详情"""
        try:
            detail = marshal(self.mongo.operation.find_one({'_id': ObjectId(operation_id)}), operation_field)
            return self.Response.return_true_data(data=detail)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()
