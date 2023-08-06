# -*- coding: utf-8 -*-

from pywe_base import BaseWechat
from pywe_storage import MemoryStorage


class BaseToken(BaseWechat):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(BaseToken, self).__init__()
        self.appid = appid
        self.secret = secret
        self.token = token
        self.storage = storage or MemoryStorage()

    def update_params(self, appid=None, secret=None, token=None, storage=None):
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.token = token or self.token
        self.storage = storage or self.storage
