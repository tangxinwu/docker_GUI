#! coding=utf-8

from django import template
import re
"""
{'10086/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '10086'}], '139/tcp': None, '21/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '21'}], '22/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '2222'}], '445/tcp': None, '80/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '8081'}], '8081/tcp': None}
"""
def rebuild_portMap(value):
    if value:
        local_port = list()
        container_port = list(value.keys())
        local_port_list = list(value.values())
        for i in local_port_list:
            try:
                for j in i:
                    local_port.append('/'.join(list(j.values())))
            except TypeError:
                local_port.append("None")
                continue
        value = ""
        #print(list(zip(local_port,container_port)))
        for i in zip(local_port,container_port):
            if i[0] != 'None':
                value += i[0] + '->' + i[1] + ','
            else:
                value += i[1] + ','
    return value


def _loop_get(value,arg):
    for i in arg.split('>'):
        value = value.get(i)
        if i == "Ports":
            value = rebuild_portMap(value)
    return value


register = template.Library()

@register.filter
def rewrite_attr(value,arg):
    """
    调整attr的显示方式
    :param value: 从docker模块中传入的值
    :param arg: containers.attr的key值
    :return:
    """
    if len(arg.split('>')) != 1:
        return _loop_get(value,arg)
    result = value.get(arg)
    if arg == 'Created':
        result = value.get(arg).split('.')[0].replace('T',' ')
    return result