#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

__version__ = '1.0'


def register_xclient(options, loop=None):
    """
    注册交互工具
    :param options: 配置项
    :param loop: for python3
    :return:
    """
    try:
        from .client3 import TradeClient3 as TradeClient
    except:
        from .client2 import TradeClient2 as TradeClient

    api_host = options.get('API_HOST')
    api_key = options.get("API_KEY")
    api_secret = options.get("API_SECRET")
    api_version = options.get("API_VERSION")

    configs = (api_key, api_secret, api_host, api_version)
    if not all(configs):
        raise KeyError('API_HOST, API_KEY, API_SECRET, API_VERSION is required')

    if TradeClient.__class__.__name__ == 'TradeClient3':
        return TradeClient(*configs, loop=loop)
    else:
        return TradeClient(*configs)


def register_xclient3(options, loop):
    """
    注册python3交互工具
    :param options:
    :param loop:
    :return:
    """
    py_version = sys.version_info
    if not py_version >= (3, 5):
        raise RuntimeError('use client3 should python >= 3.5')

    from .client3 import TradeClient3

    api_host = options.get('API_HOST')
    api_key = options.get("API_KEY")
    api_secret = options.get("API_SECRET")
    api_version = options.get("API_VERSION")

    configs = (api_key, api_secret, api_host, api_version)
    if not all(configs):
        raise KeyError('API_HOST, API_KEY, API_SECRET, API_VERSION is required')

    return TradeClient3(*configs, loop=loop)
