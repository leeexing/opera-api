# -*- coding: utf-8 -*-
"""用户模块类"""

from flask_restplus import Namespace, Resource

from app.controllers.user_c import UserManager

ns = Namespace('user', description='用户管理')
usermanager = UserManager()


@ns.route('')
class User(Resource):

    def get(self):
        """查询用户列表"""
        return usermanager.fetch_users()


@ns.route('/latest')
class UserLatest(Resource):

    def get(self):
        """查询用户列表"""
        return usermanager.fetch_latest_user()


@ns.route('/<int:user_id>')
class UserDetail(Resource):

    @ns.param('user_id', '用户ID')
    def get(self, user_id):
        """查询ID=user_id用户"""
        return usermanager.fetch_user(user_id)

    @ns.param('user_id', '用户ID')
    def put(self, user_id):
        """修改用户信息"""
        return usermanager.modify_user(user_id)

    @ns.param('user_id', '用户ID')
    def delete(self, user_id):
        """删除用户"""
        return usermanager.user_delete(user_id)


@ns.route('/avatar')
class UserAvatar(Resource):

    def post(self):
        """修改用户头像"""
        return usermanager.modify_user_avatar()
