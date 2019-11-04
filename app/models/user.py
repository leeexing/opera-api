# -*- coding: utf-8 -*-
"""用户模块"""

from hashlib import md5
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.db import MYSQL_DB as db
from app.public.enumtype import EnumUserType


class UserObject:
    """用户对象"""

    def __init__(self, userID, username, usertype, avatar=None):
        self.userID = userID
        self.username = username
        self.usertype = usertype
        self.avatar = avatar

    def __repr__(self):
        return '<User {}>'.format(self.username)


class User(db.Model):
    """用户"""
    __tablename__ = 'user'

    ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    UserName = db.Column(db.String(32), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Name = db.Column(db.String(32))
    UserType = db.Column(db.Enum(EnumUserType)) # Admin,Normal,Visitor
    CreatorId = db.Column(db.String(128))
    AvatarUrl = db.Column(db.String(128))
    CreateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ModifyTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    Remark = db.Column(db.String(256))

    def __repr__(self):
        return '<User `{}`>'.format(self.UserName)

    @property
    def password(self):
        """获取密码"""
        raise AttributeError("不可直接访问")

    @password.setter
    def password(self, passwd):
        """设置密码，之前先哈希加密处理"""
        self.Password = generate_password_hash(passwd)

    def check_password(self, passwd):
        """检测密码是否正确，和原有密码进行哈希对比"""
        return check_password_hash(self.Password, passwd)

    def generateAvatar(self, size=100):
        """生成头像
        使用用户名进行加密，可以更换
        ：size 头像的大小；默认是 100*100
        """
        digest = md5(self.UserName.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
