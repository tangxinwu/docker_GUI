#! coding=utf-8

from django import template
import re

register = template.Library()

@register.filter
def rewrite_display(value,arg=None):
    """
    调整image的显示方式
    :param value:
    :param arg:
    :return:
    """
    new_value = re.findall('\'.*\'',str(value))[0].replace("\'", '')
    return new_value
