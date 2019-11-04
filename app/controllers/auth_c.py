# -*- coding: utf-8 -*-
"""权限控制"""

import re

import requests
from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_optional

from app.public.base import BaseHandler
from app.models.user import User, EnumUserType, UserObject


class AuthManager(BaseHandler):
    """权限管理"""

    def user_login(self):
        """用户登陆"""
        try:
            user_info = request.get_json()
            self.logger.debug(user_info)
            if not user_info:
                return self.Response.return_false_data(msg='参数错误')
            username = user_info.get('userName')
            password = user_info.get('password')
            if not all([username, password]):
                return self.Response.return_false_data(msg='账号密码不完整')
            try:
                user = User.query.filter_by(UserName=username).first()
            except Exception as e:
                self.logger.error('数据库错误：%s', str(e))
                return self.Response.return_server_error()
            if not user or not user.check_password(password):
                return self.Response.return_false_data(msg='用户名不存在或密码错误')
            user_type = user.UserType.name
            user_id = user.ID
            user_obj = UserObject(userID=user_id, username=username, usertype=user_type)
            access_token = create_access_token(identity=user_obj)
            data = {
                'accessToken': access_token,
                'userName': username,
                'userID': user_id,
                'userType': user_type,
                'nickName': user.Name,
                'userAvatar': user.AvatarUrl
            }
            return self.Response.return_true_data(data=data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def user_login_by_thirdpart(self):
        """用户第三方登陆"""
        try:
            user_info = request.get_json()
            print('^-^ 用户登录信息：', user_info)
            if not user_info:
                return self.Response.return_false_data(msg='参数错误')
            username = user_info.get('username')
            password = user_info.get('password')
            nuctech_login_data = {
                'username': username,
                'password': password,
                'version': current_app.config['LOGIN_THIRDPART_VERSION']
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            res = requests.post(current_app.config['LOGIN_THIRDPART_URL'], data=nuctech_login_data, headers=headers)
            res = res.json()
            if not res.get('result'):
                return self.Response.return_false_data(msg='用户名或密码错误')
            thirdpart_info = res['package']
            auth = {
                'username': thirdpart_info['userName'],
                'userID': thirdpart_info['userID'],
                'userType': thirdpart_info['type'],
                'avatar': thirdpart_info['avatar'],
                'expires_in': thirdpart_info['expires_in'],
                'signalrToken': thirdpart_info['access_token']
            }
            identity = UserObject(userID=auth['userID'], username=auth['username'], usertype=auth['userType'], avatar=auth['avatar'])
            token = create_access_token(identity)
            data = {
                **auth,
                'accessToken': token
            }
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def logout(self):
        """退出登录"""
        return self.Response.return_true_data()

    def register(self):
        """用户注册"""
        try:
            user_info = request.get_json()
            if not user_info:
                return self.Response.return_false_data(msg='参数错误')
            username = user_info.get('userName')
            password = user_info.get('password')
            user_type = user_info.get('userType', 9)
            if not all([username, password]):
                return self.Response.return_false_data(msg='账号密码不完整！')
            if not re.match(r'[a-z, A-Z]*\d*$', password):
                return self.Response.return_false_data(msg='密码格式不正确！')
            try:
                user = User.query.filter_by(UserName=username).first()
            except Exception as e:
                self.logger.error('Database Error：%s', str(e))
                return self.Response.return_server_error()
            if user:
                return self.Response.return_false_data(msg='用户名已注册！')
            # ^添加用户
            user = User(UserName=username, Name=None, UserType=EnumUserType(int(user_type)).name)
            user.password = password
            # 自动添加头像
            user.AvatarUrl = user.generateAvatar()
            try:
                self.db.session.add(user)
                self.db.session.commit()
            except Exception as e:
                self.logger.error('Database Error：%s', str(e))
                self.db.session.rollback()
                return self.Response.return_server_error()
            data = {
                'username': user.UserName,
                'nickName': user.Name,
                'userType': user.UserType.name
            }
            return self.Response.return_true_data(data=data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    @jwt_optional
    def add_user_by_admin(self):
        """管理员添加用户

            :doc 手动添加系统用户
        """
        try:
            identity = self.get_user()
            if not identity.get('userID'):
                return self.Response.return_false_data(msg='请登陆'), 401
            userID = identity.get('userID')
            identity_type = identity.get('usertype')
            if identity_type == EnumUserType.Admin.name:
                user_info = request.get_json()
                if not user_info:
                    return self.Response.return_false_data(msg='参数错误')
                username = user_info.get('userName')
                password = user_info.get('password', '123456')
                nickname = user_info.get('nickName', username)
                user_type = user_info.get('userType', 9)
                remark = user_info.get('remark')
                if not all([username, password, user_type]):
                    return self.Response.return_false_data(msg='新建账号信息不完整')
                if not re.match(r'[a-z, A-Z]*\d*$', username):
                    return self.Response.return_false_data(msg='账号格式不正确')
                user = User.query.filter_by(UserName=username).first()
                if user:
                    return self.Response.return_false_data(msg='用户名已注册')
                # ^添加用户
                user = User(UserName=username, Name=nickname, Remark=remark,
                            CreatorId=userID, UserType=EnumUserType(int(user_type)).name)
                user.password = password
                # 自动添加头像
                user.AvatarUrl = user.generateAvatar()
                try:
                    self.db.session.add(user)
                    self.db.session.commit()
                except Exception as e:
                    self.logger.error('数据库错误：%s', str(e))
                    self.db.session.rollback()
                    return self.Response.return_server_error()
                data = {
                    'username': username,
                    'nickname': nickname
                }
                return self.Response.return_true_data(data=data)
            else:
                return self.Response.return_false_data(msg='权限不足')
        except Exception as e:
            self.logger.error('服务器错误：%s', str(e))
            return self.Response.return_server_error()
