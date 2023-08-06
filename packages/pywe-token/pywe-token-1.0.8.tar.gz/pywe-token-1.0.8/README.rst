==========
pywe-token
==========

Wechat Access Token Module for Python.

Installation
============

::

    pip install pywe-token


Usage
=====

MemoryStorage::

    Token::

        # Sandbox: http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
        In [1]: from pywe_token import Token

        In [2]: token = Token('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039')

        In [3]: token.
        token.API_DOMAIN           token.access_info_key      token.expires_at           token.storage
        token.OPEN_DOMAIN          token.access_token         token.get                  token.token
        token.WECHAT_ACCESS_TOKEN  token.appid                token.secret

        In [3]: token.access_token()
        Out[3]: u'ZhvSop2FJxAEyRLjyMIQfcfUS1tG76wGEz6hc-qgRFjaWqnLscdYBRBXVhH-SyiwXpeYTu-LfU2Fj4dTVVE3s-35MhVeaWbUMXmS3lPXgD4yrl8287yfmIXAseZI55_xUOQdADAEYA'


    access_token::

        In [1]: from pywe_token import access_token

        In [2]: access_token('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039')
        Out[2]: u'ysR7_hUtodKCF1nHjq8gFtagugB8oEOlK6hB6raMztveawVzpnqK2FtftbQGsczTj0h2kc1Gl8R7fjmGVPmXBp306WW8UZUteXqiOgxh3DL0usLRLQVRn56Oi-yigkSoSYNbAIAEKZ'


RedisStorage::

    Token::

        In [1]: import redis_extensions as redis

        In [2]: r = redis.StrictRedisExtensions(host='localhost', port=6379, db=0)

        In [3]: from pywe_storage import RedisStorage

        In [4]: storage = RedisStorage(r)

        In [5]: from pywe_token import Token

        In [6]: token = Token('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039', storage=storage)

        In [7]: token.access_token()
        Out[7]: u'5kJwbClb1CBo-5Dz_a9hZp6x_6tyDD2NnVe8mBckiv4QhB4iq13gwrplWY1fbnAE8Te_za3p6hyiJ4vG1A-hapM5PDv3PEBBIB445oxv3dShVDBXqORbCnwT37zXwEDDSITbAEANDO'

        In [8]: r.get('pywe:wx7aad305aed68bfe3:access:info')
        Out[8]: '{"access_token": "5kJwbClb1CBo-5Dz_a9hZp6x_6tyDD2NnVe8mBckiv4QhB4iq13gwrplWY1fbnAE8Te_za3p6hyiJ4vG1A-hapM5PDv3PEBBIB445oxv3dShVDBXqORbCnwT37zXwEDDSITbAEANDO", "expires_in": 7200, "expires_at": 1485104793}'


    access_token::

        In [1]: import redis_extensions as redis

        In [2]: r = redis.StrictRedisExtensions(host='localhost', port=6379, db=0)

        In [3]: from pywe_storage import RedisStorage

        In [4]: storage = RedisStorage(r)

        In [5]: from pywe_token import access_token

        In [6]: access_token('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039', storage=storage)
        Out[6]: u'5kJwbClb1CBo-5Dz_a9hZi1GcqSnLkRV2aYFmjSBTGEvVrH81XhT2eUjunVSJn_ej2uFXLJarjC0dlI78r-HxCWtTNxSPC06ARG_QqE9FoP7VhJNFsPX5z7tsySsCyEgKEZbAIAGAV'

        In [7]: r.get('pywe:wx7aad305aed68bfe3:access:info')
        Out[7]: '{"access_token": "5kJwbClb1CBo-5Dz_a9hZp6x_6tyDD2NnVe8mBckiv4QhB4iq13gwrplWY1fbnAE8Te_za3p6hyiJ4vG1A-hapM5PDv3PEBBIB445oxv3dShVDBXqORbCnwT37zXwEDDSITbAEANDO", "expires_in": 7200, "expires_at": 1485104793}'


Method
======

::

    class BaseToken(BaseWechat):
        def __init__(self, appid=None, secret=None, token=None, storage=None, expires_at=None):

    class Token(BaseToken):
        def __init__(self, appid=None, secret=None, storage=None):
            super(Token, self).__init__(appid=appid, secret=secret, storage=storage)

    def access_token(self, appid=None, secret=None, storage=None):

    def refresh_access_token(self, appid=None, secret=None, storage=None):

    def final_access_token(self, cls, appid=None, secret=None, token=None, storage=None):

