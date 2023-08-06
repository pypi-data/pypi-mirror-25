# -*- coding: utf-8 -*-

import logging
import sys
import umfpayservice

logger = logging.getLogger('umfservice')

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


def convert_url_not_encode(params):
    '''
    转化为key=value&的形式，不进行编码
    :param params: dict
    :return: str params
    '''
    if isinstance(params, list):
        iterable = params
    elif isinstance(params, dict):
        iterable = params.iteritems()
    else:
        raise TypeError("convert_url_not_encode: 不支持该类型的转化。%r" % params)

    result = None
    for key, value in iterable:
        if value is None or value == '':
            continue

        if result is None:
            result = "%s=%s" % (key, value)
        else:
            result = "%s&%s=%s" % (result, key, value)
    return result

def utf8(value):
    if isinstance(value, unicode) and sys.version_info < (3, 0):
        return value.encode('utf-8')
    else:
        return value
