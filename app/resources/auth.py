# -*- coding: utf-8 -*-
"""权限控制"""

from flask_restplus import Namespace, Resource

from app.controllers.auth_c import AuthManager

ns = Namespace('auth', description='权限管理')
authmanager = AuthManager()


@ns.route('/login')
class Login(Resource):

    def post(self):
        """用户登录"""
        return authmanager.user_login()


@ns.route('/login/nuctech')
class LoginThirdPart(Resource):

    def post(self):
        """用户登录"""
        return authmanager.user_login_by_thirdpart()


@ns.route('/logout')
class Logout(Resource):

    def post(self):
        """退出登录"""
        return authmanager.logout()


@ns.route('/register')
class Registe(Resource):

    def post(self):
        """用户注册  -- 暂时不开放"""
        return authmanager.register()


@ns.route('/addUser')
class AddUserByAdmin(Resource):

    def post(self):
        """管理员添加用户"""
        return authmanager.add_user_by_admin()
