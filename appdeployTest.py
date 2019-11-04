# -*- coding: utf-8 -*-
"""部署主文件<测试环境>"""

from app.main import create_app

APP = create_app(env='TEST')


if __name__ == '__main__':
    APP.run()
