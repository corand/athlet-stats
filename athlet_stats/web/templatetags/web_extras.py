from django import template
import datetime

register = template.Library()


def totime(value):
    """converts from seconds to hh:mm:ss.mm"""
    return  str(datetime.timedelta(microseconds=value))

register.filter('totime', totime)