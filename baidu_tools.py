#!/usr/bin/env python
# coding: utf-8

# baidu voice open api for chinese 
# fit for python 3

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import requests
import base64
import json
import os

__all__ = [
    'baiduYuyin',
]

class baiduYuyin(object):

    APIURI_TOKEN = "https://openapi.baidu.com/oauth/2.0/token"
    APIURI_TTS = "http://tsn.baidu.com/text2audio"
    APIURI_ASR = "http://vop.baidu.com/server_api"
    DEVICE_ID = "202cb962ac59075b964b07152d234b70" # you can change it for anyone

    def __init__(self,api_key,secret_key):
        self.API_Key = api_key
        self.Secret_Key = secret_key

    def get_token(self):
        token_post_data = {"grant_type": "client_credentials", "client_id": self.API_Key, "client_secret": self.Secret_Key}
        r = requests.post(baiduYuyin.APIURI_TOKEN, data=token_post_data, timeout=10)
        response = json.loads(r.text)
        return response['access_token']
    
    def text2sound(self,input_text, file_name):
        baidu_token = self.get_token()
        sound_post_data = {"tex": input_text, "lan": "zh", "tok": baidu_token, "ctp": 1, "cuid": baiduYuyin.DEVICE_ID, "spd": 5, "pit": 5, "vol": 5, "per": 0}
        r = requests.post(baiduYuyin.APIURI_TTS, data=sound_post_data, stream=True, timeout=10)
        with open(file_name, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)
        return True
    
    def sound2text(self,file_name):
        baidu_token = self.get_token()
        f = open(file_name,'rb');
        raw_data = f.read()
        raw_lenth = os.path.getsize(file_name)
        post_data = {'format':'wav','rate':8000,'channel':1,'cuid':baiduYuyin.DEVICE_ID,'token':baidu_token,'lan':'zh','speech':base64.b64encode(raw_data),'len':raw_lenth}
        headers = {'Content-Type':'application/json'}
        r = requests.post(baiduYuyin.APIURI_ASR,data=json.dumps(post_data),headers=headers)
        if r.status_code == 200:
            response = json.loads(r.text)
            if response["err_no"] == 0:
               return response["result"]
            else:
               print("API ERROR, error no: %d" %(response["err_no"]))
               return []
        else:
            print("CALL ERROR, status code: %d" % (r.status_code))
            return []
