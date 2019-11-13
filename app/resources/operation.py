# -*- coding: utf-8 -*-
"""运维数据"""

from flask_restplus import Namespace, Resource

from app.controllers.operation_c import OperationManager

ns = Namespace('operation', description='歌剧院运维数据周报表')
operationManager = OperationManager()


@ns.route('')
class OperationResource(Resource):

    def get(self):
        """获取运维数据列表"""
        return operationManager.fetch_operaion_list()


@ns.route('/<string:operation_id>')
class OperationDetailResource(Resource):

    def get(self, operation_id):
        """获取运维数据具体某周的详情"""
        return operationManager.fetch_operaion_detail(operation_id)
