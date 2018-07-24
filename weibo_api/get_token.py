#coding:utf-8
import sys
from weibo_api.sinaweibopy.weibo import APIClient
# from weibo_api.sinaweibopy.weibo import SinaWeiboMixin      # suppose you are using Twitter
import json
import webbrowser
import io
import time
import datetime
# sys.setdefaultencoding('utf-8')
APP_KEY =''
APP_SECRET = ''
CALLBACK_URL = ''
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
print(url)
SOME_CODE= input("输入code:")
r = client.request_access_token(SOME_CODE)
print(r)
access_token = r["access_token"]
expires = r["expires_in"]
print(datetime.datetime.fromtimestamp(expires))
print(access_token)
print(expires)
"""


"""


""