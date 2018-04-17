#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import logging
import re
import codecs
import time

logger = logging.getLogger("AppName")

def setLogger(logger):
    formatter = logging.Formatter('%(asctime)s %(filename)-10s[line:%(lineno)d]%(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler("logger%s.log" % time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time())))
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

def toSecond(strTime):
    return time.mktime(time.strptime(strTime, "%Y-%m-%d %H:%M:%S"))

setLogger(logger)

fileName = "e:\\prjs\\n60\\EVENT_2018-04-16 11_03_28 AM.csv"
if not os.path.exists(fileName):
    logger.error("file not exists:" + fileName)
    sys.exit()

print "start paring..."

timeStap=[]
keyWord="HEARTBEAT_JS"
with codecs.open(fileName, 'r') as f:
    for line in f.readlines():
        p = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(HEARTBEAT_JS)')
        match = re.match(p, line)
        if match is not None:
            timeStap.append(match.group(1))

last = toSecond(timeStap.pop(0))
for t in timeStap:
    timesec = toSecond(t)
    d = timesec - last
    if d < 4*60 or d > 6*60:
        logger.error('heartbeat not normal in time ' + t)
    last = timesec

