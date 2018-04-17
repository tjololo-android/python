# -*- coding: UTF-8 -*-
import json
import requests
import sys

def loginImeEvent(username, password):
        url = 'http://192.168.1.103:8099/api/login'
        data = {
            'password': password,
            'userName': username,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'http://192.168.1.103:8099/'
        }
        content = mySession.post(url, data=data, headers=headers).text

        print content
 #       return json.loads(content[1: -1])

mySession = requests.Session()
username = "suyong"
password = "123456"
loginImeEvent(username, password)
