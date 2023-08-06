#!/usr/bin/python
# -*- coding: utf-8 -*-
import aiohttp

from xclient.common import TradeClient
from xclient.errors import ERROR_ITEMS


class TradeClient3(TradeClient):

    def __init__(self, app_key, app_secret, api_host, api_version, loop=None):
        super(TradeClient3, self).__init__(app_key, app_secret, api_host, api_version)
        self.session = aiohttp.ClientSession(loop=loop)

    async def get(self, path, params=None, request_id=None, session_id=None):
        url = '{}{}'.format(self.api_host, path)
        params, headers = self.build_params_headers(params, request_id, session_id)

        async with self.session.get(url, params=params, headers=headers) as resp:
            return await self._parse_resp(resp)

    async def post(self, path, params=None, request_id=None, session_id=None):
        url = '{}{}'.format(self.api_host, path)
        params, headers = self.build_params_headers(params, request_id, session_id)

        async with self.session.get(url, params=params, headers=headers) as resp:
            return await self._parse_resp(resp)

    async def _parse_resp(self, resp):
        status_code = resp.status
        if 300 > status_code >= 200:
            return await resp.json()
        else:
            return ERROR_ITEMS.get(status_code)
