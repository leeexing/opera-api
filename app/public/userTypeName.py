# -*- coding: utf-8 -*-

from app.models.user import EnumUserType


def usertypename(usertype):
    """获取用户类型"""
    if usertype == EnumUserType.Admin:
        return '管理员'
    if usertype == EnumUserType.Normal:
        return '普通用户'
    if usertype == EnumUserType.Tester:
        return '开发测试'
    if usertype == EnumUserType.TopicMaker:
        return '考题制作者'
    else:
        return '游客'
