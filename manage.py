# -*- coding: utf-8 -*-
"""主控模块
   ~~~~~~~~

    ：主要用于开发环境
"""

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app.main import create_app
from app.models.user import User
from app.db import MYSQL_DB as db


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='0.0.0.0', port=6281, use_debugger=True))
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    """初始化shell环境变量
    将db, app, User加入上下文中
    """
    return dict(app=app, db=db, User=User)


@manager.command
def seed():
    """初始化用户"""
    user = User(UserName='admin', UserType=1)
    user.password = 'admin'
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
