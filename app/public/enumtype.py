# -*-coding: utf-8 -*-
"""枚举类型数据"""

from enum import Enum


class EnumUserType(Enum):
    """用户角色"""

    Admin    = 1
    Normal   = 2
    Tester  = 3
    TopicMaker = 4
    Visitor  = 9


class EnumCaptureImageStatus(Enum):
    """采集图像是否被处理"""

    UnHandle = 0
    Handling = 1
    Handled  = 2


class TenementIndustry(Enum):
    """租户所属行业"""

    Training = '培训'
    Airplane = '机场'
    Bus      = '公交'
    Subway   = '地铁'
    Customs  = '海关'
    Server   = '其他'


class UploadStatus(Enum):
    """文件上传的各个状态"""

    Disabled  = 0
    Transcode = 1
    Finished  = 2

