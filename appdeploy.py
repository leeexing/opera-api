# -*- coding: utf-8 -*-
"""部署主文件<测生产环境>"""

from app.main import create_app

APP = create_app(env='PROD')


if __name__ == '__main__':
    APP.run()
