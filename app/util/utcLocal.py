# -*- coding: utf-8 -*-
"""时间处理模块"""

import time
from datetime import datetime


def utc_local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st.strftime('%Y-%m-%d %H:%M:%S.%f')


def local_utc(local_st):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.utcfromtimestamp(time_struct)
    return utc_st


def time_field_type(time_str):
    """格式化时间
        2018-11-13T16:22:25.7562285+08:00
        转换成
        2018-08-07 14:22:40.815644
    """
    time_str = time_str[0:-7].replace('T', ' ')
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
