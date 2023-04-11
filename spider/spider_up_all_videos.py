#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/11 19:28
# @Author : Seeumt
# @File : up_videos.py
from bs4 import BeautifulSoup
import requests
import urllib
import re
import csv
import time
from pandas import  DataFrame
from utils.FakeUserAgentUtil import FakeUserAgentUtil
fua = FakeUserAgentUtil()
import pandas as pd
# 39627524(264) 427457465(11)






aidList = []
oidList = []
titleList = []
playList = []
descriptionList = []
videoReviewList = []
lengthList = []
commentList = []
def getOid(aid):
    UserAgent = fua.genFakeUserAgent()
    headers = {
        "User-Agent": UserAgent,
    }
    response = requests.get(
        "https://www.bilibili.com/widget/getPageList?aid="+str(aid), headers=headers)
    return response.json()

def getTotalPageCount(videoCount):
    pageCount = 0
    if videoCount % 100 == 0 & videoCount >= 100:
        pageCount = videoCount // 100
    else:
        pageCount = videoCount // 100 + 1
    return pageCount

def getVideoCount(mid):
    return getRes(mid,1).get('data').get('page').get('count')

def getRes(mid,currentPage):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    response = requests.get(
        "https://api.bilibili.com/x/space/arc/search?pn="+str(currentPage)+"&ps=100&order=click&keyword=&mid="+str(mid), headers=headers)
    return response.json()

if __name__ == '__main__':
    totalPage = getTotalPageCount(getVideoCount(39627524))
    videoList = []
    for currentPage in range(totalPage):
        vlist = getRes(39627524,currentPage+1).get('data').get('list').get('vlist')
        videoList[len(videoList):len(videoList)] = vlist
    for video in videoList:
        print(video)
        title = video.get('title')
        titleList.append(title)
        aid = video.get('aid')
        aidList.append(aid)
        oid = getOid(aid)[0].get('cid')
        oidList.append(oid)
        description = getOid(aid)[0].get('description')
        descriptionList.append(description)
        play = getOid(aid)[0].get('play')
        playList.append(play)
        comment = getOid(aid)[0].get('comment')
        commentList.append(comment)
        videoReview = getOid(aid)[0].get('video_review')
        videoReviewList.append(videoReview)
        length = getOid(aid)[0].get('length')
        lengthList.append(length)

    data = {
            'title': titleList,
            'aid': aidList,
            'oid': oidList,
            'description':descriptionList,
            'play':playList,
            'video_review':videoReviewList,
            'length':lengthList
            }
    frame = DataFrame(data)
    frame.to_csv("C:\\Users\\Seeumt\\Desktop\\blibli_videos_all.csv", encoding="utf_8_sig", index=False)
    # 测试单个
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    # }
    # response = requests.get(
    #     "https://www.bilibili.com/widget/getPageList?aid=456082081", headers=headers)
    # print(response.json()[0].get('cid'))

