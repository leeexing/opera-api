# -*- coding: utf-8 -*-
"""
    参数配置
    ~~~~~~~

    : marshal_with 解析
    ：expect 添加
"""

from flask_restplus import reqparse

from app.util.utcLocal import time_field_type

# -原图像数据接口参数解析
ORIGIN_IMAGE_PARSER = reqparse.RequestParser()
ORIGIN_IMAGE_PARSER.add_argument('TaskID', required=True)
ORIGIN_IMAGE_PARSER.add_argument('FacilityCode')
ORIGIN_IMAGE_PARSER.add_argument('PackageCode')
ORIGIN_IMAGE_PARSER.add_argument('OssStoreKey')
ORIGIN_IMAGE_PARSER.add_argument('StorageSize', type=int)
ORIGIN_IMAGE_PARSER.add_argument('FilterTag', type=int)
ORIGIN_IMAGE_PARSER.add_argument('TaskStatus', type=int)
ORIGIN_IMAGE_PARSER.add_argument('UploadElapsedTime', type=float)
ORIGIN_IMAGE_PARSER.add_argument('GaitherTime', type=time_field_type)
ORIGIN_IMAGE_PARSER.add_argument('UploadTime', type=time_field_type)

# -授权请求头
authorization = reqparse.RequestParser()
authorization.add_argument('Authorization', required=True, location='headers')

# -分页
PAGING_PARSER = reqparse.RequestParser()
PAGING_PARSER.add_argument('page', type=int, default=1)
PAGING_PARSER.add_argument('limit', type=int, default=10)

# -图像查询
IMAGE_QUERY_PARSER = reqparse.RequestParser()
IMAGE_QUERY_PARSER.add_argument('viewCount', type=int, default=0)
IMAGE_QUERY_PARSER.add_argument('imageName')
