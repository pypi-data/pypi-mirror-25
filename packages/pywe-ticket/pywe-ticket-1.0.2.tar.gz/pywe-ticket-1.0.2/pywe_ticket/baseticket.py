# -*- coding: utf-8 -*-

from pywe_token import BaseToken


class BaseTicket(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        super(BaseTicket, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        self.type = type

    def update_params(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.token = token or self.token
        self.type = type or self.type
        self.storage = storage or self.storage
