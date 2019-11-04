# -*- coding: utf-8 -*-
"""输出帮助模块"""


class ResponseHelper:
    """输出帮助类"""
    @staticmethod
    def return_true_data(data=None, msg='success', status=200, **kwargs):
        """返回正确结果"""
        result = {
            "result": True,
            "status": status,
            "data": data,
            "msg": msg,
            **kwargs
        }
        return result

    @staticmethod
    def return_false_data(data=None, msg="error", status=200, **kwargs):
        """返回错误结果"""
        return {
            "result": False,
            "status": status,
            "data": data,
            "msg": msg,
            **kwargs
        }

    @staticmethod
    def return_server_error(data=None, msg="Server Error", status=500, **kwargs):
        """返回服务器错误"""
        return {
            "result": False,
            "status": status,
            "msg": msg,
            "data": data,
            **kwargs
        }, 500
