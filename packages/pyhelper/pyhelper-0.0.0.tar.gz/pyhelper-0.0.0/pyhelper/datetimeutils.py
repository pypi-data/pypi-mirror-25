# coding=utf-8

import datetime


def to_date_object(date):
    """
    转换对象为日期对象
    :param date:
    :return:
    """
    if date is None:
        return None

    if isinstance(date, str):
        n = len(date)
        if 8 == n:
            fmt = '%Y%m%d'
        elif 10 == n:
            pos = date.find('/')
            if -1 == pos:
                fmt = '%Y-%m-%d' if 4 == date.find('-') else '%m-%d-%Y'
            elif 4 == pos:
                fmt = '%Y/%m/%d'
            else:
                fmt = '%m/%d/%Y'
        else:
            fmt = '%Y-%m-%d %H:%M:%S'
        date = datetime.datetime.strptime(date, fmt)

    if not isinstance(date, datetime.date):
        raise TypeError('date type error!' + str(date))
    return date


def is_same_day(d1, d2):
    """
    判断两个日期是同一天，忽略时分秒
    :param d1:
    :param d2:
    :return: bool
    """
    d1 = to_date_object(d1)
    d2 = to_date_object(d2)
    return d1.year == d2.year and d1.month == d2.month and d1.day == d2.day


def is_same_or_later_day(d1, d2):
    """
    判断d2是否等于或晚于d1，忽略时分秒
    :param d1:
    :param d2:
    :return: bool
    """
    d1 = to_date_object(d1)
    d2 = to_date_object(d2)
    d1 = d1.year * 10000 + d1.month * 100 + d1.day
    d2 = d2.year * 10000 + d2.month * 100 + d2.day

    return d2 >= d1
