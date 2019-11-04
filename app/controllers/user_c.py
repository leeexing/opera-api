# -*- coding: utf-8 -*-
"""用户业务类"""

from flask import request, current_app
from flask_jwt_extended import jwt_required

from app.util.storage import qiniu_storage
from app.public.base import BaseHandler
from app.public.userTypeName import usertypename
from app.models.user import User, EnumUserType


class UserManager(BaseHandler):
    """用户业务类"""

    @jwt_required
    def fetch_users(self):
        """用户列表查询"""
        try:
            identity = self.get_user()
            skip, limit = self.get_paging_parser()
            if not identity.get('userID'):
                return self.Response.return_false_data(msg='请登录')
            user_type = identity.get('usertype')
            if user_type != EnumUserType.Admin.name:
                return self.Response.return_false_data(msg='权限不足', status=403)
            query_info = self.parser_args()
            name = query_info.get('username', '')
            if name:
                users = User.query.filter(User.UserName.like(
                    name + '%')).offset(skip).limit(limit).all()
            else:
                users = User.query.offset(skip).limit(limit).all()
            total = User.query.count()
            users_list = [dict(userId=user.ID, userName=user.UserName, name=user.Name, usertype=user.UserType.value,
                                usertypeName=usertypename(user.UserType), createTime=str(user.CreateTime)) for user in users]
            data = {
                'users': users_list,
                'total': total
            }
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    @jwt_required
    def fetch_user(self, user_id):
        """用户详情"""
        try:
            identity = self.get_user()
            if not identity.get('userID'):
                return self.Response.return_false_data(msg='请登录')
            user = User.query.filter_by(ID=int(user_id)).first()
            if not user:
                return self.Response.return_false_data(msg='未知用户', status=401)
            user_data = {
                'userID': user.ID,
                'userName': user.UserName,
                'nickName': user.Name,
                'userType': user.UserType.name,
                'userAvatar': user.AvatarUrl
            }
            return self.Response.return_true_data(user_data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    @jwt_required
    def fetch_latest_user(self):
        """用户刷新前端页面，获取最新的用户详情
            不需要传入用户ID（传入用户ID可能时被用户篡改的，那么获取的用户信息就不同了，权限系统也不一样）
        """
        try:
            identity = self.get_user()
            if not identity.get('userID'):
                return self.Response.return_false_data(msg='请登录')
            user_id = identity.get('userID')
            user = User.query.filter_by(ID=int(user_id)).first()
            user_data = {
                'userID': user.ID,
                'userName': user.UserName,
                'nickName': user.Name,
                'userType': user.UserType.name,
                'userAvatar': user.AvatarUrl
            }
            return self.Response.return_true_data(user_data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    @jwt_required
    def modify_user(self, user_id):
        """用户信息修改"""
        try:
            identity = self.get_user()
            if not identity.get('userID'):
                return self.Response.return_false_data(msg='请登录！')
            user_type = identity.get('usertype')
            if user_type != EnumUserType.Admin.name:
                return self.Response.return_false_data(msg='权限不足！', status=403)
            user_info = self.parser_json()
            user_type_modify = user_info.get('usertype')
            if not all([user_id, user_type_modify]):
                return self.Response.return_false_data(msg='参数错误!')
            try:
                User.query.filter_by(ID=user_id).update(
                    {'UserType': EnumUserType(user_type_modify)})
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                self.logger.error('Database Error: %s', str(e))
                return self.Response.return_server_error()
            return self.Response.return_true_data('用户类型修改成功!')
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    @jwt_required
    def delete_user(self, user_id):
        """删除用户"""
        try:
            identity = self.get_user()
            if not identity.get('userID'):
                return self.Response.return_false_data(msg='请登录!')
            identity_type = identity.get('usertype')
            if identity_type != EnumUserType.Admin.name:
                return self.Response.return_false_data(msg='权限不足!', status=403), 403
            if not user_id:
                return self.Response.return_false_data(msg='参数错误!')
            user = User.query.filter_by(ID=user_id).first()
            if not user:
                return self.Response.return_false_data('用户不存在!')
            try:
                self.db.session.delete(user)
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                self.logger.error('Database Error: %s', str(e))
                return self.Response.return_server_error()
            return self.Response.return_true_data('用户删除成功!')
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    @jwt_required
    def modify_user_avatar(self):
        """用户头像上传"""
        try:
            identity = self.get_user()
            username = identity.get('username')
            avatar = request.files.get('avatar')
            if not avatar:
                return self.Response.return_false_data(msg='图像未上传!')
            avatar_data = avatar.read()
            try:
                image_name = qiniu_storage(avatar_data)
            except Exception as e:
                self.logger.error('上传七牛云错误：%s', str(e))
                return self.Response.return_false_data(msg='七牛云图片上传失败!')
            avatar_url = current_app.config['QINIU_DOMAIN_PREFIX'] + image_name
            try:
                User.query.filter_by(UserName=username).update(
                    {'AvatarUrl': avatar_url})
                self.db.session.commit()
            except Exception as e:
                self.db.session.rollback()
                self.logger.error('Database Error: %s', str(e))
                return self.Response.return_false_data(msg='用户头像保存失败!')
            data = {
                'avatarUrl': avatar_url,
                'avatarName': image_name
            }
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()
