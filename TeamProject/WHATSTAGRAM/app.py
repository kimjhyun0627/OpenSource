#!usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os.path
import random

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from elasticsearch import Elasticsearch
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

import time
import re
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
es_host = "http://localhost:9200"
es = Elasticsearch(hosts=es_host)


@app.route('/', methods=['GET'])
def home():
    create_tagfolder('static/tag_folder/')
    ids = getid()
    return render_template('main.html')


@app.route('/view', methods=['GET'])
def crawl():
    word = request.args.get("ID")
    tags = []
    freqs = []
    if (create_tagfolder('static/tag_folder/' + word) == 0):
        tags, freqs = instagram_crawling(word)
    else:
        tags, freqs = get_es(word)
        counter(word)

    imgs = []
    for t in tags:
        imgs.append('tag_folder/' + word + '/' + t + '/tagIMG.jpg')

    return render_template('show.html', id=word, tagList=tags, freqList=freqs,
                           profile='tag_folder/' + word + '/profile/profile.jpg', imgList=imgs)


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument("headless")  # 백그라운드작업
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def create_tagfolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return 0
    except:
        return -1


def create_index(word):
    if not es.indices.exists(index=word):
        return es.indices.create(index=word)


def instagram_crawling(ID):
    # webdriver 설정하기

    # put application's code here
    # word = input("아이디 입력: ")
    word = str(ID)
    url = 'https://www.picuki.com/profile/' + word

    # chrome
    # br = webdriver.Chrome()
    br = set_chrome_driver()
    br.set_window_size(1500, 1000)

    # br.implicitly_wait(20)
    time.sleep(random.randrange(0, 3))

    suc = False
    count = 3
    while suc != True and count >= 0:
        time.sleep(2)
        count -= 1
        try:
            br.get(url)
            doc = {"name": word, "freq": 1}
            es.index(index="id", document=doc)
            # 해당 페이지의 div 클래스 id를 추출후 # 추가
            wait = WebDriverWait(br, 10)
            html = br.page_source
            # print(html)
            soup = BeautifulSoup(html, 'lxml')
            profile = soup.find('div', 'profile-avatar').find('img')
            post = soup.find('ul', 'box-photos profile-box-photos clearfix').find_all('img')
            # print(post)
            suc = True
        except:
            suc = False
            continue

    if suc == False:
        return 0

    # print(id)
    tag_list = []
    human_list = []
    tag_freq = []
    human_freq = []

    create_tagfolder(f'static/tag_folder/' + word + '/profile')
    imgurl = profile.get("src")
    req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})
    with open(f'static/tag_folder/{word}/profile/profile.jpg', 'wb') as h:
        img = urlopen(req).read()
        h.write(img)

    n = 1
    create_index(word)
    for i in post:
        # time.sleep(2)
        # br.execute_script("window.scrollTo(0, 500);")

        try:
            list = i.get('alt').split()
            print(list)
            for j in list:
                if '#' in j:
                    print("j: " + j)
                    if not os.path.exists(f'static/tag_folder/{word}/{j}'):
                        # 각 태그에 해당하는 디렉토리 생성(없을때만)
                        tag_list.append(j)
                        tag_freq.append(1)
                        create_tagfolder(f'static/tag_folder/' + word + '/' + j)
                        imgurl = i.get("src")
                        req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})

                        # 각 태그에 해당하는 이미지 저장
                        with open(f'static/tag_folder/{word}/{j}/' + 'tagIMG.jpg', 'wb') as h:
                            img = urlopen(req).read()
                            h.write(img)
                            n = n + 1
                            # time.sleep(2)
                    else:
                        tag_freq[tag_list.index(j)] = tag_freq[tag_list.index(j)] + 1

                elif '@' in j:
                    human_list.append(j)
                    human_freq.append(1)
        except:
            continue

        # print(i.get("src"))
        print("=" * 80)

    print(tag_list)
    print(tag_freq)

    tag_list, tag_freq = sortList(tag_list, tag_freq)
    # human_list, human_freq = sortList(human_list, human_freq)

    tag_list, tag_freq = randList(tag_list, tag_freq)
    # human_list, human_freq = randList(human_list, human_freq)

    for i in range(0, len(tag_list)):
        body = {"tag": tag_list[i], "freq": tag_freq[i]}
        print(body)
        es.index(index=word, document=body)

    print(tag_list)
    print(tag_freq)

    print(human_list)
    print(human_freq)

    # br.close()
    br.quit()

    return tag_list[0:4], tag_freq[0:4]

    # 크롤링할 게시물 행 by 열 범위 지정
    # br.execute_script("window.scrollTo(0, 500);")


def sortList(sig, freq):
    for i in range(0, len(sig) - 1):
        idx = i
        for j in range(i + 1, len(sig)):
            if freq[j] > freq[idx]:
                idx = j
                print(sig[idx])
                print(sig[i])
        sig[i], sig[idx] = sig[idx], sig[i]
        freq[i], freq[idx] = freq[idx], freq[i]
    print("-" * 90)
    print(sig)
    print(freq)
    return sig, freq


def randList(sig, freq):
    i = 0
    while i < len(sig):
        top = i
        bottom = i
        check = False
        randList = []
        tmpList = []
        for j in range(top + 1, len(sig)):
            if freq[i] == freq[j]:
                bottom = j
                check = True
        if check == False:
            if freq[top] != freq[top + 1]:
                i += 1
                continue
            else:
                bottom = len(sig) - 1
        tmpList.append(sig[top:bottom + 1])
        print(tmpList)
        i = bottom + 1

        for k in range(top, bottom + 1):
            ran_num = random.randint(0, bottom - top)
            while ran_num in randList:
                ran_num = random.randint(0, bottom - top)
            randList.append(ran_num)
            print(ran_num)
            sig[k] = tmpList[0][ran_num]
    print('+' * 90)
    print(sig)
    print(freq)

    return sig, freq


def get_es(word):
    res = es.search(index=word, size=4)

    dicList = []
    freqList = []
    for i in res['hits']['hits']:
        i = list(i.values())
        dic = list(i[3].values())[0]
        freq = list(i[3].values())[1]
        dicList.append(dic)
        freqList.append(freq)
    print(dicList)

    return dicList, freqList


def getid():
    res = es.search(index="id", size=10000)
    idList = []
    freqList = []
    for i in res['hits']['hits']:
        i = list(i.values())
        id = list(i[3].values())[0]
        freq = list(i[3].values())[1]
        idList.append(id)
        freqList.append(freq)
    print(idList)
    print(freqList)

    idList, freqList = sortList(idList, freqList)
    idList, freqList = randList(idList, freqList)

    print(idList)
    print(freqList)


def counter(word):
    res = es.search(index="id", body={"size": 1, 'query': {'match': {"name": word}}})
    res = list(res['hits']['hits'][0].values())
    print(res)
    ID = res[1]
    name = list(res[3].values())[0]
    freq = list(res[3].values())[1]
    print(ID)
    print(name)
    print(freq)
    es.update(index="id", id=ID, doc={"name": name, "freq": freq + 1})


# 오류1 : 글 자체가 없으면 findAll() 에러
# 오류2 : 게시물 갯수가 적으면 에러
# 오류3 : 비공계 처리 어떻게 할건지

if __name__ == "__main__":
    app.run(debug=True)
