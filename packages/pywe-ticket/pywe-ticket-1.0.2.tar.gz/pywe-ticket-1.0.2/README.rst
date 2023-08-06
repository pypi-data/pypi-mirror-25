===========
pywe-ticket
===========

Wechat Ticket Module for Python.

Installation
============

::

    pip install pywe-ticket


Usage
=====

MemoryStorage::

    Ticket::

        # Sandbox: http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
        In [1]: from pywe_ticket import Ticket

        In [2]: ticket = Ticket('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039')

        In [3]: ticket.
        ticket.API_DOMAIN       ticket.WECHAT_TICKET    ticket.expires_at       ticket.refresh_ticket   ticket.ticket           ticket.type
        ticket.MCH_DOMAIN       ticket.api_ticket       ticket.get              ticket.secret           ticket.ticket_info_key
        ticket.OPEN_DOMAIN      ticket.appid            ticket.jsapi_ticket     ticket.storage          ticket.tickets

        In [3]: ticket.ticket()
        Out[3]: u'sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6irBzC2ySEv3Ofex5q2eY1C50R-GffnrsRWFI7uDim9g'

        In [4]: ticket.jsapi_ticket()
        Out[4]: u'sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6irBzC2ySEv3Ofex5q2eY1C50R-GffnrsRWFI7uDim9g'

        In [5]: ticket.api_ticket()
        Out[5]: u'E0o2-at6NcC2OsJiQTlwlEaNeSfCJatHbnTsr44R0i4GASKTn-ZELWB3Oe7cpRbg5bLf4ZD5Ylg5cuOqma8LxA'


    ticket::

        In [1]: from pywe_ticket import ticket, api_ticket, jsapi_ticket

        In [2]: ticket('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039')
        Out[2]: u'sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6irBzC2ySEv3Ofex5q2eY1C50R-GffnrsRWFI7uDim9g'

        In [3]: api_ticket('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039')
        Out[3]: u'E0o2-at6NcC2OsJiQTlwlEaNeSfCJatHbnTsr44R0i4GASKTn-ZELWB3Oe7cpRbg5bLf4ZD5Ylg5cuOqma8LxA'

        In [4]: jsapi_ticket('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039')
        Out[4]: u'sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6irBzC2ySEv3Ofex5q2eY1C50R-GffnrsRWFI7uDim9g'


RedisStorage::

    Ticket::

        In [1]: import redis_extensions as redis

        In [2]: r = redis.StrictRedisExtensions(host='localhost', port=6379, db=0)

        In [3]: from pywe_storage import RedisStorage

        In [4]: storage = RedisStorage(r)

        In [5]: from pywe_ticket import Ticket

        In [6]: ticket = Ticket('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039', storage=storage)

        In [7]: ticket.ticket()
        Out[7]: u'sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6-KN0maRl2mp5Gn8-ah5WDDphfA-zyZ4AfBb3Q13O8LA'

        In [8]: r.get('pywe:wx7aad305aed68bfe3:jsapi:ticket:info')
        Out[8]: '{"ticket": "sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6-KN0maRl2mp5Gn8-ah5WDDphfA-zyZ4AfBb3Q13O8LA", "expires_at": 1499767753, "expires_in": 7200, "errcode": 0, "errmsg": "ok"}'


    ticket::

        In [1]: import redis_extensions as redis

        In [2]: r = redis.StrictRedisExtensions(host='localhost', port=6379, db=0)

        In [3]: from pywe_storage import RedisStorage

        In [4]: storage = RedisStorage(r)

        In [5]: from pywe_ticket import ticket

        In [6]: ticket('wx7aad305aed68bfe3', '9eac636765940ec286055c559ff84039', storage=storage)
        Out[6]: u'sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6-KN0maRl2mp5Gn8-ah5WDDphfA-zyZ4AfBb3Q13O8LA'

        In [7]: r.get('pywe:wx7aad305aed68bfe3:jsapi:ticket:info')
        Out[7]: '{"ticket": "sM4AOVdWfPE4DxkXGEs8VB_Ml7aLXlo2_KgFGduwNU6-KN0maRl2mp5Gn8-ah5WDDphfA-zyZ4AfBb3Q13O8LA", "expires_at": 1499767753, "expires_in": 7200, "errcode": 0, "errmsg": "ok"}'


Method
======

::

    class Ticket(BaseWechat):
        def __init__(self, appid=None, secret=None, type='jsapi', storage=None):

    def ticket(self, appid=None, secret=None, token=None, type='jsapi', storage=None):

    def api_ticket(self, appid=None, secret=None, token=None, storage=None):

    def jsapi_ticket(self, appid=None, secret=None, token=None, storage=None):

    def refresh_ticket(self, appid=None, secret=None, token=None, type='jsapi', storage=None):

