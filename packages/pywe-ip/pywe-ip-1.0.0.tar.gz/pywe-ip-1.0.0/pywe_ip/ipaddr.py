# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class WechatIP(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(WechatIP, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 获取微信服务器IP地址, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140187
        self.WECHAT_IPS = self.API_DOMAIN + '/cgi-bin/getcallbackip?access_token={access_token}'

    def wechat_ips(self, appid=None, secret=None, token=None, storage=None):
        return self.get(self.WECHAT_IPS, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage))


ipaddr = WechatIP()
wechat_ips = ipaddr.wechat_ips
