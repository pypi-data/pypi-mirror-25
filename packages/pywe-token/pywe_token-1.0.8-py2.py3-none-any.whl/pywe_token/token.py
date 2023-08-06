# -*- coding: utf-8 -*-

import time

from pywe_exception import WeChatException

from .basetoken import BaseToken


class Token(BaseToken):
    def __init__(self, appid=None, secret=None, storage=None):
        super(Token, self).__init__(appid=appid, secret=secret, storage=storage)
        # 获取access token, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140183
        self.WECHAT_ACCESS_TOKEN = self.API_DOMAIN + '/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'

    @property
    def access_info_key(self):
        return '{0}:access:info'.format(self.appid)

    def __about_to_expires(self, expires_at):
        return expires_at and expires_at - int(time.time()) < 60

    def __fetch_access_token(self, appid=None, secret=None, storage=None):
        # Update Params
        self.update_params(appid=appid, secret=secret, storage=storage)
        access_info = self.get(self.WECHAT_ACCESS_TOKEN, appid=self.appid, secret=self.secret)
        if 'expires_in' not in access_info:
            raise WeChatException(access_info)
        expires_in = access_info.get('expires_in')
        if self.storage:
            access_info['expires_at'] = int(time.time()) + expires_in
            self.storage.set(self.access_info_key, access_info, expires_in)
        return access_info.get('access_token')

    def access_token(self, appid=None, secret=None, storage=None):
        # Update Params
        self.update_params(appid=appid, secret=secret, storage=storage)
        # Fetch access_info
        access_info = self.storage.get(self.access_info_key)
        if access_info:
            access_token = access_info.get('access_token')
            if access_token and not self.__about_to_expires(access_info.get('expires_at')):
                return access_token
        return self.__fetch_access_token(appid, secret, storage)

    def refresh_access_token(self, appid=None, secret=None, storage=None):
        return self.__fetch_access_token(appid, secret, storage)

    def final_access_token(self, cls=None, appid=None, secret=None, token=None, storage=None):
        return token or self.access_token(appid or cls.appid, secret or cls.secret, storage=storage or cls.storage)


token = Token()
access_token = token.access_token
refresh_access_token = token.refresh_access_token
final_access_token = token.final_access_token
