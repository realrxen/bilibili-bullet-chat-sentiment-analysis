#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/11 23:56
# @Author : Seeumt
# @File : bullet.py
from bs4 import BeautifulSoup
import requests
import urllib
import re
import csv
import time, datetime
from pandas import  DataFrame
import pandas as pd
import os.path
from utils.FakeUserAgentUtil import FakeUserAgentUtil
fua = FakeUserAgentUtil()

def getBullet(oid):
    userAgent = fua.genFakeUserAgent()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    # 208343921 205250485
    return requests.get("https://api.bilibili.com/x/v1/dm/list.so?oid="+str(oid), headers=headers)
def csv2JsonList():
    import sys
    import json
    input_file = "C:\\Users\\Seeumt\\Desktop\\blibli_videos3.csv"
    lines = ""
    # 读取文件
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    keys = lines[0].split(',')
    line_num = 1
    total_lines = len(lines)
    # 数据存储
    datas = []
    while line_num < total_lines:
        values = lines[line_num].split(",")
        datas.append(dict(zip(keys, values)))
        line_num = line_num + 1
    return datas
if __name__ == '__main__':
    videos = csv2JsonList()
    for video in videos:
        oid = video.get("oid")
        response = getBullet(oid)
        print(response)
        html_doc = response.content.decode('utf-8')
        bs = BeautifulSoup(html_doc, "html.parser")
        # soup = BeautifulSoup(html_get("href")doc,'lxml')
        tagD = bs.find_all("d")
        format = re.compile("<d.*?>(.*?)</d>")
        DanMu = format.findall(str(tagD))
        times = []
        senders = []
        danMuIds = []
        oids = []
        for tag in tagD:
            oids.append(oid)
            timestamp = int(tag.get("p").split(",")[4])
            timeArray = time.localtime(timestamp)
            time1 = time.strftime("%Y-%m-%d", timeArray)
            times.append(time1)
            sender = tag.get("p").split(",")[6]
            senders.append(sender)
            danMuId = tag.get("p").split(",")[7]
            danMuIds.append(danMuId)
        data = {'time': times,
                'content': DanMu,
                'oid':oids,
                'sender':senders,
                'danMuId':danMuIds
                }
        frame = DataFrame(data)

        isFileExist = os.path.isfile("C:\\Users\\Seeumt\\Desktop\\bullet10.csv")
        if isFileExist:
            frameOld = pd.read_csv("C:\\Users\\Seeumt\\Desktop\\bullet10.csv", encoding='utf-8')
            frameNew = frameOld.append(frame)
            frameNew.to_csv("C:\\Users\\Seeumt\\Desktop\\bullet10.csv", encoding="utf_8_sig", index=False)
        else:
            frame.to_csv("C:\\Users\\Seeumt\\Desktop\\bullet10.csv", encoding="utf_8_sig", index=False)
        
