#coding=utf-8

import datetime

def to_date_object(date):
    """
    转换对象为日期对象
    :param date:
    :return:
    """
    if date is None: return None
    if isinstance(date, str):
        n = len(date)
        if 8 == n:
            format = '%Y%m%d'
        elif 10 == n:
            pos = date.find('/')
            if -1 == pos:
                format = '%Y-%m-%d' if 4 == date.find('-') else '%m-%d-%Y'
            elif 4 == pos:
                format = '%Y/%m/%d'
            else:
                format = '%m/%d/%Y'
        else:
            format = '%Y-%m-%d %H:%M:%S'
        date = datetime.datetime.strptime(date, format)

    if not isinstance(date, datetime.date):
        raise TypeError('date type error!' + str(date))
    return date
