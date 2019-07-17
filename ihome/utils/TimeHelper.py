# -*- coding:utf-8 -*-

import datetime
import math


def parse(time_str):
    try:
        time_str = str(time_str)
        time_str = time_str.replace("/", "-")
        time_str = time_str.replace('"', '')
        if time_str == "0":
            return datetime.datetime.now()
        elif time_str == "":
            return datetime.datetime.now()
        elif time_str.count(".") >= 1:
            return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
        elif time_str.count(":") == 1:
            return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        elif time_str.count(":") == 0:
            return datetime.datetime.strptime(time_str, '%Y-%m-%d')
        elif time_str.lower().count("am") > 0 or time_str.lower().count("pm") > 0:
            return datetime.datetime.strptime(time_str, '%Y-%m-%d %I:%M:%S %p')
        else:
            return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    except Exception as ex:
        return datetime.datetime.now()


def now():
    return datetime.datetime.now()


def format_time(tm, only_to_minute=True):
    if not isinstance(tm, datetime.datetime):
        return ""
    if tm is not None:
        if only_to_minute:
            return tm.strftime('%Y-%m-%d %H:%M')
        else:
            return tm.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ""


def format_timespan(span_time, zero_time=now()):
    delta_t = span_time - zero_time
    days = int(delta_t.days)
    hours = int((delta_t.total_seconds() - days * 60.0 * 60.0 * 24) / 60 / 60)
    minutes = int((delta_t.seconds / 60) % 60.0)
    last_time = str(days) + u'天' + str(hours) + u'小时' + str(minutes) + u'分钟'
    return last_time


def calculate_timespan(date_str):
    zero_time = now()
    span_time = parse(date_str)
    delta_t = round((zero_time - span_time).total_seconds())
    c_month = round(delta_t / (60 * 60 * 24 * 30))
    c_day = round(delta_t / (60 * 60 * 24))
    c_hour = round(delta_t / (60 * 60))
    c_min = round(delta_t / 60)

    if c_month >= 1:
        result = str(int(c_month)) + u'个月前'
    elif c_day >= 1:
        result = str(int(c_day)) + u'天前'
    elif c_hour >= 1:
        result = str(int(c_hour)) + u'个小时前'
    elif c_min >= 1:
        result = str(int(c_min)) + u'分钟前'
    else:
        result = u'刚刚'

    return result
