# -*- coding: utf-8 -*-
"""图像分发批次"""

from flask_restplus import Namespace, Resource

from app.public.fields import batch_field
from app.controllers.batch_c import BatchManager


ns = Namespace('batch', description='图像分发批次号')
batch_model = ns.model('batch', batch_field)
batchManager = BatchManager()


@ns.route('')
class BatchResource(Resource):

    def get(self):
        """获取所有批次"""
        return batchManager.fetch_batches()


@ns.route('/<string:batch_id>')
class BatchResource2(Resource):

    @ns.expect(batch_model)
    def get(self, batch_id):
        """获取ID=batch_id批次"""
        return batchManager.fetch_batch(batch_id)

    def put(self, batch_id):
        """修改ID=batch_id批次"""
        return batchManager.modify_batch(batch_id)

    def delete(self, batch_id):
        """删除ID=batch_id批次"""
        return batchManager.delete_batch(batch_id)


@ns.route('/<string:batch_id>/images')
class ImagesOfBatch(Resource):

    def get(self, batch_id):
        return batchManager.fetch_batch_images(batch_id)
