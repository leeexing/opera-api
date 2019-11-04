# -*- coding: utf-8 -*-
"""jwt初始化

    ：TODO 后面几个loader貌似没有起作用。不知为何
"""

from flask import jsonify


class BindJwt():
    """初始化jwt相关数据"""

    @staticmethod
    def init(jwt):

        @jwt.user_identity_loader
        def user_identity_lookup(identity):
            """用户身份信息提取：最好是包含除了用户信息的其他信息
                from flask_jwt_extended import get_jwt_identity
            """
            return {
                'userID': identity.userID,
                'username': identity.username,
                'usertype': identity.usertype
            }

        # @jwt.user_claims_loader
        # def add_claims_to_access_token(identity):
        #     """获取用户角色类型:访问令牌信息简单到只有用户信息最好
        #     from flask_jwt_extended import get_jwt_claims
        #     """
        #     print(identity)
        #     return identity
        #     # return {
        #     #     'userID': identity.userID,
        #     #     'username': identity.username,
        #     #     'usertype': identity.usertype
        #     # }

        @jwt.expired_token_loader
        def my_expired_token_callback():
            """token过期：返回特定的数据格式
            """
            return jsonify({
                'data': None,
                'msg': 'The token has expired'
            }), 401

        @jwt.invalid_token_loader
        def invalid_token_callback(err_str=None):
            """无效token"""
            return jsonify({
                'data': None,
                'msg': err_str if err_str else '无效Token'
            }), 401

        @jwt.unauthorized_loader
        def unauthorized_callback(err_str=None):
            """非法Token返回结果"""
            return jsonify({
                'data': None,
                'msg': err_str if err_str else '未授权'
            }), 401

        @jwt.revoked_token_loader
        def revoked_token_callback():
            """已撤销Token"""
            return jsonify({
                'data': None,
                'msg': '您的账号已在其他地方登录'
            }), 401
