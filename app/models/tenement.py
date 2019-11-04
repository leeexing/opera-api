# -*- coding: utf-8 -*-
"""租户数据模型"""

from datetime import datetime

from app.db import MYSQL_DB as db


class Tenement(db.Model):
    """租户模型"""

    __tablename__ =  'tenement'

    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    CompanyID = db.Column(db.String(100)) # 企业编码
    Industry = db.Column(db.String(100)) # 所属行业
    Remark = db.Column(db.String(300))
    CreateTime = db.Column(db.DateTime, default=datetime.now)
    ModifyTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Tenement: {}>'.format(self.Name)


class TbUser(db.Model):
    """租户子用户模型"""

    __bind_key__ = 'tenement' # -连接到指定的数据库
    __tablename__ =  'TbUser'

    ID = db.Column(db.Integer, primary_key=True,nullable=False)
    AccountNo = db.Column(db.String(20), nullable=False)
    Avatar = db.Column(db.String(50))
    BirthDay = db.Column(db.DateTime)
    CreateTime = db.Column(db.DateTime, nullable=False)
    ModifyTime = db.Column(db.DateTime, nullable=False)
    Education = db.Column(db.Integer)
    IDCard = db.Column(db.String(18))
    IsDelete = db.Column(db.Integer)
    JobNo = db.Column(db.String(50))
    Mobile = db.Column(db.String(50))
    Name = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(200), nullable=False)
    Sex = db.Column(db.Integer)
    Theme = db.Column(db.Integer)
    Timestamp = db.Column(db.String(50))
    Type = db.Column(db.Integer)
    FaceID = db.Column(db.String(30))
    WeChatOpenID = db.Column(db.String(30))
    # 外键
    Grade = db.Column(db.Integer)
    OrgID = db.Column(db.Integer)
    Post = db.Column(db.Integer)

    def __repr__(self):
        return '<TBUser: {}>'.format(self.Name)
