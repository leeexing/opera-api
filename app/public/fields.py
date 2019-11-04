# -*- coding: utf-8 -*-
"""格式化字段名"""

from datetime import datetime

from flask_restplus import fields


# -采集图像
capture_image_field = {
    'TaskID': fields.String(example='nuctech00001', description='上传任务唯一ID'),
    'FacilityCode': fields.String(example='beijing54541', description='终端设备编号'),
    'PackageCode': fields.String(example='4658713245', description='实际包号'),
    'OssStoreKey': fields.String(example='storage&^$%^&*()', description='存储标识值'),
    'StorageSize': fields.Integer(example=2048, description='包大小KB'),
    'FilterTag': fields.Integer(default=0, description='筛图的标记，0表示未经过筛图的，1表示经过筛图而上传的'),
    'TaskStatus': fields.Integer(default=0, description='原图像处理状态（0：未处理，1：处理中，2：处理完成）'),
    'UploadElapsedTime': fields.Float(example=123456.789, description='上传耗时'),
    'GaitherTime': fields.DateTime(example='2018-08-07T14:22:40.8156442+08:00', description='采集时间'),
    'UploadTime': fields.DateTime(example='2018-11-13T16:22:25.7562285+08:00', description='上传时间'),
}


# -采集图像:响应
capture_image_res_field = {
    'ID': fields.Integer(description='ID'),
    **capture_image_field
}


# -租户
tenement_field = {
    'ID': fields.String(example='123', description='ID'),
    'Name': fields.String(example='杭州地铁', description='租户名称'),
    'CompanyID': fields.String(example='4658713245', description='企业编码'),
    'Industry': fields.String(example='海关', description='所属行业'),
    'Remark': fields.String(default='', example='这是一个很重要的租户', description='备注'),
    'CreateTime': fields.DateTime(example='2018-12-24T14:22:40.8156442+08:00', description='添加时间'),
    'ModifyTime': fields.DateTime(example='2018-12-25T14:22:40.8156442+08:00', description='修改时间'),
}


# -图像批次【mysql】<暂时不用>
batch_field = {
    'ID': fields.String(example='123', description='ID'),
    'Name': fields.String(example='首都机场第一批', description='批次名称'),
    'BatchID': fields.String(example='9d7578b6-0a4f-11e9-997f-28f10e170840', description='批次号'),
    'TenementID': fields.String(example='300', description='租户ID'),
    'BatchType': fields.String(example='dr', description='分发类型'), # - all、ct、dr
    'Description': fields.String(),
    'CreateTime': fields.DateTime(example='2018-12-24T14:22:40.8156442+08:00', description='添加时间'),
    'ModifyTime': fields.DateTime(example='2018-12-25T14:22:40.8156442+08:00', description='修改时间'),
}


# -图像基本信息
image_base_info = {
    'id': fields.String(attribute='_id'),
    'storageId': fields.String(),
    'imageName': fields.String(),
    'description': fields.String(),
    'createTime': fields.String(attribute=lambda img: img['createTime'].strftime('%Y-%m-%d %H:%M:%S.%f')),
    'modifyTime': fields.String(attribute=lambda img: img['modifyTime'].strftime('%Y-%m-%d %H:%M:%S.%f')),
}


# -图像批次【mongo】
image_batch_field = {
    'id': fields.String(attribute='_id'),
    'name': fields.String(example='首都机场第一批', description='批次名称'),
    'batchID': fields.String(example='9d7578b6-0a4f-11e9-997f-28f10e170840', description='批次号'),
    'storageIds': fields.List(fields.String), # - 图像存储ID
    'tenementName': fields.String(example='300', description='租户名称'),
    'batchType': fields.String(example='dr', description='分发类型(all、ct、dr)'),
    'packageId': fields.String(description='图像包的ID(如果是通过图像包分发的话)'),
    'packageName': fields.String(description='图像包名称'),
    'description': fields.String(description='批次描述'),
    'createTime': fields.String(attribute=lambda img: img['createTime'].strftime('%Y-%m-%d %H:%M:%S.%f')),
    'modifyTime': fields.String(attribute=lambda img: img['modifyTime'].strftime('%Y-%m-%d %H:%M:%S.%f'))
}

# -图像包
image_package_field = {
    'id': fields.String(attribute='_id'),
    'packageName': fields.String(),
    'storageIds': fields.List(fields.String),
    'tags': fields.List(fields.String),
    'userID': fields.String(),
    'creator': fields.String(),
    'description': fields.String(),
    'createTime': fields.String(attribute=lambda img: img['createTime'].strftime('%Y-%m-%d %H:%M:%S.%f')),
    'modifyTime': fields.String(attribute=lambda img: img['modifyTime'].strftime('%Y-%m-%d %H:%M:%S.%f')),
}

# -租户的用户
tbuser_field = {
    'AccountNo': fields.String(),
    'Avatar': fields.String(),
    'BirthDay': fields.String(),
    'CreateTime': fields.String(),
    'ModifyTime': fields.String(),
    'Education': fields.Integer(),
    'IDCard': fields.String(),
    'IsDelete': fields.String(),
    'JobNo': fields.String(),
    'Mobile': fields.String(),
    'Name': fields.String(),
    # 'Password': fields.String(),
    'Sex': fields.Integer(),
    'Theme': fields.Integer(),
    # 'Timestamp': fields.String(attribute=lambda x: bytes(x.Timestamp)),
    'Type': fields.Integer(),
    'FaceID': fields.String(),
    'WeChatOpenID': fields.String(),
    'Grade': fields.Integer(),
    'OrgID': fields.Integer(),
    'Post': fields.Integer()
}

# -文件管理
file_field = {
    'id': fields.String(attribute='_id'),
    'md5': fields.String(),
    'status': fields.Integer(),
    'thumbnail': fields.String(),
    'url': fields.String(),
    'length': fields.Integer(),
}

# -图像：可根据项目环境动态改变图像url的host地址
def create_imginfo_field(prefix=''):

    ct_field = {
        'url': fields.String(attribute=lambda x: prefix + x['url'] if x['url'] else x['url']),
        'volumeData': fields.String(attribute=lambda x: prefix + x['volumeData'] if x['volumeData'] else x['volumeData']),
        'suspect': fields.String(attribute=lambda x: prefix + x['suspect'] if x['suspect'] else x['suspect']),
        'density': fields.String(attribute=lambda x: prefix + x['density'] if x['density'] else x['density']),
    }

    dr_field = {
        'url': fields.String(attribute=lambda x: prefix + x['url'] if x['url'] else x['url']),
        'perspective': fields.String(),
        'suspect': fields.String(attribute=lambda x: prefix + x['suspect'] if x['suspect'] else x['suspect']),
    }

    thumbnail_field = {
        'url': fields.String(attribute=lambda x: prefix + x['url'] if x['url'] else x['url']),
        'thumbnail': fields.String(attribute=lambda x: prefix + x['thumbnail'] if x['thumbnail'] else x['thumbnail']),
        'type': fields.String(),
    }

    image_field = {
        'id': fields.String(attribute='_id'),
        'name': fields.String(),
        'version': fields.String(),
        'ct': fields.Nested(ct_field, default=[]),
        'dr': fields.List(fields.Nested(dr_field)),
        'thumbnails': fields.List(fields.Nested(thumbnail_field), default=[]),
        'physicalMaps': fields.List(fields.Nested(thumbnail_field), default=[]),
    }
    return image_field
