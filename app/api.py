# -*- coding: utf-8 -*-
"""swagger-api
    ~~~~~~~~~~~

    ：主要使用flask-restplus进行restful-api
"""

from flask_restplus import Api

from app.resources.auth import ns as auth_api
from app.resources.home import ns as home_api
from app.resources.user import ns as user_api
from app.resources.operation import ns as operation_api

api = Api(
    title='Opera API',
    version='1.0',
    prefix='/v1/api',
    description='Opera platform for anp'
)

api.add_namespace(auth_api)
api.add_namespace(user_api)
api.add_namespace(home_api)
api.add_namespace(operation_api)
