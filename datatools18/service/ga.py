
import conf.common as config
import math
import urllib
import requests
import json

from datetime import datetime
# from apiclient.discovery import build
# from google.oauth2.service_account import Credentials

from service.models import *
"""
[
    'v'      :1,
    'tid'    :'UA-52479722-1',
    'cid'    :'555',
    't'      :'transaction',
    'ti'     :'9998',
    'tr'     :'100',
    'tt'     :'10',       налоги
    'cu'     :'AUD',     валюта
    'pa'     :'purchase',
    'pr[1]id':'1',
    'pr[1]nm':'Test Product',
    'pr[1]ca':'Test Category',
    'pr[1]qt':'2',
    'pr[1]pr':'100',
    'cd1':'Сustom Dimension 1'
    dh Document Host,
    dp Document Path
]
"""

class gaTracker:

    def __init__(self):
        """Constructor"""
        self.url = "https://ssl.google-analytics.com/collect"
        self.ver = 1

    def sendPageview(self, cid, tid, dh, dp, context, function):
        """Формирование строки для отправки"""

        cd2 = str(int(datetime.now().strftime('%Y%m%d%H%M%S')))

        hit = {'v':self.ver,
                't':'pageview',
                'tid':tid,
                'cid': cid,
                'dh':dh,
                'dp':dp,
                'cd1':cid,
                'cd2':cd2,
                'cd3':context,
                'cd4':function
            }

        params = urllib.parse.urlencode(hit)
        url = '{}?{}'.format(self.url, params)

        requests.post(url)

        return url


    def storeInput(self, user_id, messenger_id, content, context, function):
        """Разбор входящего сообщения"""
        cid = user_id
        dh = config.ga_host
        tid =  config.ga_tracker
        source = config.messengers_id[messenger_id]
        try:
            if content is not None:
                dp = str(content)
            else:
                dp = 'not_set'

        except Exception as e:
            dp = str(e) + 'error'

        dp = 'human_{}: {}'.format(source,dp)
        url = self.sendPageview(cid, tid, dh, dp, context, function)

        return  url


    def storeOutput(self, user_id, messenger_id, content):
        """Разбор исходящего сообщения"""

        def modify_content(content):
            try:
                r = content['text']
            except Exception as e:
                r = str(content)
            return r

        content = modify_content(content)
        dh = config.ga_host
        tid =  config.ga_tracker
        cid = user_id
        source = config.messengers_id[messenger_id]
        try:
            if content is not None:
                dp = content
            else:
                dp = 'not_set'
        except Exception as e:
            dp = str(e) + 'error'

        dp = 'bot_{}: {}'.format(source,dp)

        url = self.sendPageview(cid, tid, dh, dp, 'bot_context', 'bot_function')

        return  url


    def storeOutputTg(self, message_id, message):
        """Разбор исходящего сообщения"""
        url = '-'
        dh = config.ga_host
        tid =  config.ga_tracker
        cid = message_id

        try:
            page_state = getattr(message, 'state', '')
            page_text = getattr(message, 'text', 'not_set')
            dp = '{} {}'.format(page_state,page_text).strip()

        except Exception as e:
            dp = str(e) + 'error'

        dp = 'bot_tg: {}'.format(dp)

        url = self.sendPageview(cid, tid, dh, dp, 'context','function')

        return  url
