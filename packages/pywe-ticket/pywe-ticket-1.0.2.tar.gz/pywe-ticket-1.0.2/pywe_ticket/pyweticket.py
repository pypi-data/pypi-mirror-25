# -*- coding: utf-8 -*-

import time

from pywe_exception import WeChatException
from pywe_token import final_access_token

from .baseticket import BaseTicket


class Ticket(BaseTicket):
    def __init__(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        super(Ticket, self).__init__(appid=appid, secret=secret, token=token, type=type, storage=storage)
        # 微信JS-SDK说明文档, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141115
        self.WECHAT_TICKET = self.API_DOMAIN + '/cgi-bin/ticket/getticket?access_token={access_token}&type={type}'

    @property
    def ticket_info_key(self):
        return '{0}:{1}:ticket:info'.format(self.appid, self.type)

    def __about_to_expires(self, expires_at):
        return expires_at and expires_at - int(time.time()) < 60

    def __fetch_ticket(self, appid=None, secret=None, token=None, type=None, storage=None):
        # Update Params
        self.update_params(appid=appid, secret=secret, token=token, type=type, storage=storage)
        # Ticket Info Request
        ticket_info = self.get(self.WECHAT_TICKET, access_token=final_access_token(self, appid=self.appid, secret=self.secret, token=self.token, storage=self.storage), type=self.type)
        # Request Error
        if 'expires_in' not in ticket_info:
            raise WeChatException(ticket_info)
        # Set Ticket Info into Storage
        expires_in = ticket_info.get('expires_in')
        ticket_info['expires_at'] = int(time.time()) + expires_in
        self.storage.set(self.ticket_info_key, ticket_info, expires_in)
        # Return Ticket
        return ticket_info.get('ticket')

    def ticket(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        # Update Params
        self.update_params(appid=appid, secret=secret, token=token, type=type, storage=storage)
        # Fetch ticket_info
        ticket_info = self.storage.get(self.ticket_info_key)
        if ticket_info:
            ticket = ticket_info.get('ticket')
            if ticket and not self.__about_to_expires(ticket_info.get('expires_at')):
                return ticket
        return self.__fetch_ticket(appid, secret, token, type, storage)

    def api_ticket(self, appid=None, secret=None, token=None, storage=None):
        """ 卡券 api_ticket """
        return self.ticket(appid, secret, token, 'wx_card', storage)

    def jsapi_ticket(self, appid=None, secret=None, token=None, storage=None):
        return self.ticket(appid, secret, token, 'jsapi', storage)

    def refresh_ticket(self, appid=None, secret=None, token=None, type='jsapi', storage=None):
        return self.__fetch_ticket(appid, secret, token, type, storage)


ticketcls = Ticket()
ticket = ticketcls.ticket
api_ticket = ticketcls.api_ticket
jsapi_ticket = ticketcls.jsapi_ticket
refresh_ticket = ticketcls.refresh_ticket
