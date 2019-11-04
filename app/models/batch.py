# -*- coding: utf-8 -*-
"""图像分发批次"""

from datetime import datetime

from app.db import MYSQL_DB as db


class Batch(db.Model):
    """批次模型"""

    __tablename__ = 'batch'

    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(45))
    BatchID = db.Column(db.String(100), nullable=False)
    BatchType = db.Column(db.String(10), nullable=False)
    Description = db.Column(db.String(300))
    CreateTime = db.Column(db.DateTime, default=datetime.now)
    ModifyTime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    TenementID = db.Column(db.Integer, db.ForeignKey('tenement.ID'))
    tenements = db.relationship('Tenement', backref='batch', lazy='select')

    def __repr__(self):
        return '<Batch `{}`>'.format(self.BatchID)


class BatchImage(db.Model):
    """批次-图像 （批次中包含的图像进行关联）"""

    __tablename__ = 'batch_image'

    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    ImageID = db.Column(db.String(45), nullable=False)
    BatchID = db.Column(db.String(45), nullable=False)
    BatchType = db.Column(db.String(10), default='all')

    def __repr__(self):
        return '<BatchImage `{}`>'.format(self.BatchID)
