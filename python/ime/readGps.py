#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import threading
import time
import json
import uuid
import base64
import gzip
import re
from cStringIO import StringIO

class Context():
    def __init__(self, imei):
        self.imei = imei
        self.acessToken = None
        self.im_ip = None
        self.im_port = None
        self.sid = None

class Client():
    def __init__(self, imei):
        self.ctx = Context(imei)
        self.ctx.sid = str(uuid.uuid1())

    def getToken(self, username, password):
        url = "http://api.szime.com/oauth/token?grant_type=device&client_id=app&client_secret=api1234&scope=SCOPE_READ&username=" + username + "&password=" + password
        heads = dict(ContentType="text/html;charset=UTF-8")
        result = requests.get(url, heads)
        if 200 != result.status_code:
            print "response status code is not 200"
            return False

        try:
            response = json.loads(result.content)
            self.ctx.acessToken = response["access_token"]
            self.ctx.im_ip = response["im_ip"]
            self.ctx.im_port = response["im_port"]
            return True
        except Exception as e:
            print e
        return False

    def post(self, cmd, param):
        url = "http://" + self.ctx.im_ip + ":9182" + "?access_token=" + self.ctx.acessToken
        self.ctx.sid = str(uuid.uuid1())

        deviceCmd = self.composeDeviceCommand(cmd, param)
        serviceCmd = self.composeServiceCommand("cmd", deviceCmd)
        response = None
        try:
            data = json.dumps(serviceCmd)
            heads = {
                "ContentType": "application/json",
                "ContentLength": str(len(data))
            }
            response = requests.post(url, headers=heads, data=data)
        except Exception as e:
            print e
        if response is not None and response.status_code == 200:
            return response.content.decode("utf-8")
        else:
            print None

    # {  "_cmd": "cmd",  "id": "35291202046210",  "data": {    "CMD": "getxxx",    "PARAM": {      "type": "version"    },    "DID": "35291202046210",    "SID": "16c7e5b0-ed3c-4719-9987-34c54ea0050c"  },  "timeout": 30000}
    def composeServiceCommand(self, cmd, data):
        return {"_cmd":cmd, "id":self.ctx.imei, "data":data,"timeout":30000}

    #{    "CMD": "getxxx",    "PARAM": {      "type": "version"    },    "DID": "35291202046210",    "SID": "16c7e5b0-ed3c-4719-9987-34c54ea0050c"  },
    def composeDeviceCommand(self, cmd, param):
        return {"CMD":cmd, "PARAM":{"type": param}, "DID":self.ctx.imei, "SID":self.ctx.sid}

class Worker(threading.Thread):
    def __init__(self, imei):
        threading.Thread.__init__(self)
        self.imei=imei
        self.interval = INTERVAL
        self.period = PERIOD

    def getGpsData(self):
        try:
            response = self.client.post("getInfo", "GPS")
            gpsData = json.loads(response)["data"]["PARAM"]["VAL"]
            gpsStr = gzip_uncompress(decodeb64(gpsData))

            snr = re.findall(r'Snr\'\s*:\s*(\d+\.\d)', gpsStr)
            snr.sort(key=float, reverse=True)
            if len(snr) > 3:
                snr = snr[0:3]

            #{u'head': 170, u'E': 1, u'TS': 1523512006151L, u'longtitude': 113946263, u'N': 1, u'isFixed': 1, u'time': 1523512009, u'latitude': 22544133, u'Satellites': [{u'Elevation': 6, u'Prn': 3, u'Snr': 38.5, u'hasEphemeris': False, u'Azimuth': 222}, {u'Elevation': 2, u'Prn': 7, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 311}, {u'Elevation': 53, u'Prn': 8, u'Snr': 20.200000762939453, u'hasEphemeris': False, u'Azimuth': 211}, {u'Elevation': 28, u'Prn': 9, u'Snr': 41.29999923706055, u'hasEphemeris': False, u'Azimuth': 309}, {u'Elevation': 9, u'Prn': 11, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 197}, {u'Elevation': 5, u'Prn': 14, u'Snr': 25.700000762939453, u'hasEphemeris': False, u'Azimuth': 156}, {u'Elevation': 41, u'Prn': 16, u'Snr': 35, u'hasEphemeris': False, u'Azimuth': 21}, {u'Elevation': 9, u'Prn': 18, u'Snr': 22.899999618530273, u'hasEphemeris': False, u'Azimuth': 180}, {u'Elevation': 6, u'Prn': 21, u'Snr': 14.300000190734863, u'hasEphemeris': False, u'Azimuth': 54}, {u'Elevation': 4, u'Prn': 22, u'Snr': 22.5, u'hasEphemeris': False, u'Azimuth': 201}, {u'Elevation': 56, u'Prn': 23, u'Snr': 23, u'hasEphemeris': False, u'Azimuth': 270}, {u'Elevation': 24, u'Prn': 26, u'Snr': 40.099998474121094, u'hasEphemeris': False, u'Azimuth': 49}, {u'Elevation': 80, u'Prn': 27, u'Snr': 23.600000381469727, u'hasEphemeris': False, u'Azimuth': 58}, {u'Elevation': 20, u'Prn': 31, u'Snr': 23.600000381469727, u'hasEphemeris': False, u'Azimuth': 111}, {u'Elevation': 20, u'Prn': 32, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 111}, {u'Elevation': 12, u'Prn': 65, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 308}, {u'Elevation': 15, u'Prn': 71, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 210}, {u'Elevation': 26, u'Prn': 72, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 261}, {u'Elevation': 29, u'Prn': 73, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 62}, {u'Elevation': 36, u'Prn': 74, u'Snr': 13.5, u'hasEphemeris': False, u'Azimuth': 358}, {u'Elevation': 9, u'Prn': 75, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 310}, {u'Elevation': 19, u'Prn': 83, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 33}, {u'Elevation': 60, u'Prn': 84, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 90}, {u'Elevation': 35, u'Prn': 85, u'Snr': 0, u'hasEphemeris': False, u'Azimuth': 175}], u'speed': 0}
            gpsData = json.loads(gpsStr)
            t = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(gpsData["time"]))
            print self.imei, t, gpsData["isFixed"], gpsData["speed"], snr, gpsData["longtitude"], gpsData["latitude"]
        except Exception as e:
            print e

    def run(self):
        self.client = Client(self.imei)
        if not self.client.getToken(self.imei, self.imei):
            print "get Token failed"
            return

        times = 1
        while True:
            print "%d times get gps data..." % times
            times += 1
            self.getGpsData()
            if self.timeout():
                break

    def timeout(self):
        if(self.period > 0):
            self.period -= self.interval
            time.sleep(self.interval)
            return False
        else:
            return True

def encodeb64(str):
    return base64.b64encode(str)

def decodeb64(str):
    return base64.b64decode(str)

def gzip_compress(raw_data):
    buf = StringIO()
    f = gzip.GzipFile(mode='wb', fileobj=buf)
    try:
        f.write(raw_data)
    finally:
        f.close()
    return buf.getvalue()

def gzip_uncompress(c_data):
    buf = StringIO(c_data)
    f = gzip.GzipFile(mode='rb', fileobj=buf)
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data

def main():
    imeis=[
        "35629601551861",
        "35629601649479",
        "35629601170645",
        "35291202009425",
        "35419703011228",
        "35291202046210",
    ]

    threads=[]
    for i in imeis:
        t = Worker(i);
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print "test gps end"

INTERVAL = 60 #second
PERIOD = 3*24*3600 #hour

main()

# if __name__ == 'main':
#     main()
