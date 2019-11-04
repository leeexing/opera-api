# -*- coding: utf-8 -*-
"""文件扫描后台进程
    ~~~~~~~~~~~~

    功能：定期扫描`FILE_SERVICE_STATIC_URL`文件夹里面的文件
    import os
    import shutil

    os.remove(path) #删除文件
    os.removedirs(path) #删除空文件夹

    shutil.rmtree(path) #递归删除文件夹
"""

import os
import time
import shutil
from threading import Thread
from datetime import timedelta, datetime

from app.conf.config import Config

BASE_URL = Config.FILE_SERVICE_UPLOAD_PHYSICS_URL
# BASE_URL = os.path.dirname(os.path.abspath('__file__')) + r'\app\static\files'
TIME_TO_REMOVE = timedelta(days=1)


def scan_file_2_remove():
    """检查文件是否大于两天，大于将文件删除"""
    while True:
        file_list = os.listdir(BASE_URL)
        print('清理缓存文件列表：', file_list)
        for file_name in file_list:
            file_path = os.path.join(BASE_URL, file_name)
            t = os.path.getctime(file_path)
            now = datetime.fromtimestamp(time.time())
            file_create_time = datetime.fromtimestamp(t)
            if now - file_create_time > TIME_TO_REMOVE:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        time.sleep(60*60)

def bind_thread():
    t = Thread(target=scan_file_2_remove, name='scanFile')
    t.setDaemon(True)
    t.start()
