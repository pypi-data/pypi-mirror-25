#coding=utf-8

import datetime
from datetime import timedelta
from functools import lru_cache

import requests

import time


@lru_cache()
def is_holiday(day):
    """
    判断是否节假日, api 来自百度 apistore: http://apistore.baidu.com/apiworks/servicedetail/1116.html
    :param day: 日期， 格式为 '20160404'
    :return: bool
    """
    api = 'http://tool.bitefu.net/jiari/'
    params = {'d': day, 'apiserviceid': 1116}
    rep = requests.get(api, params)
    res = rep.text
    return True if res != "0" else False


def is_holiday_today():
    """
    判断今天是否时节假日
    :return: bool
    """
    today = datetime.date.today().strftime('%Y%m%d')
    return is_holiday(today)