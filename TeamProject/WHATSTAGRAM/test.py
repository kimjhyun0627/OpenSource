#해당 id 의 닉네임 , posts, follwers , folloing 크롤링
#!usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
es_host = "http://localhost:9200"
profile_list = []

# 닉네임, 포스트 수 , 팔로워 , 팔로잉 수 크롤링
def crawl_profile(id):
    id = id.replace('@', '')
    url = 'https://www.picuki.com/profile/' + id

    time.sleep(2)

    # 해당 페이지의 div 클래스 id를 추출후 # 추가
    temp = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    des = soup.find('h2', 'profile-name-bottom').get_text()
    #des2 = soup.find('div', 'profile-description').get_text()
    followers = soup.find('span' , 'followed_by').get_text()
    following = soup.find('span', 'follows').get_text()
    profile_post = soup.find('span', 'total_posts').get_text()
    temp.append(des)
    #temp.append(des2)
    temp.append(profile_post)
    temp.append(followers)
    temp.append(following)
    profile_list.append(temp)