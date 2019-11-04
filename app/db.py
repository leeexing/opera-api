# -*- coding: utf-8 -*-
"""数据库模块"""

from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

MYSQL_DB = SQLAlchemy()
MONGO_DB = PyMongo()
