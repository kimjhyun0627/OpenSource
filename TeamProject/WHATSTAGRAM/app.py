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
es = Elasticsearch(hosts=es_host, timeout=30, max_retries=3, retry_on_timeout=True)


@app.route('/', methods=['GET'])
def main_page():
    tag_folder_creater('static/tag_folder/')
    ids, freqs = es_ids_getter()
    imgs = []
    for i in ids:
        if i != "":
            imgs.append('tag_folder/' + i + '/profile/profile.jpg')
    print(imgs)

    return render_template('main_semi.html', idList=ids, imgList=imgs)


@app.route('/view', methods=['GET'])
def info_page():
    word = request.args.get("ID")
    word = word.lower()
    if (tag_folder_creater('static/tag_folder/' + word) == 0):
        tags, freqs, ids = instagram_crawler(word)
    else:
        tags, freqs, ids = es_data_getter(word)
        print(ids)
        if (tags != -1):
            es_freq_counter(word)

    # if tags==0 and freqs == 0 and ids == 0:

    if tags == -1 and freqs == -1 and ids == -1:
        return render_template('Error_show.html')

    imgs = []
    for t in tags:
        if t != "":
            imgs.append('tag_folder/' + word + '/' + t + '/tagIMG.jpg')
        else:
            imgs.append("")
    for i in ids:
        if i != "":
            imgs.append('tag_folder/' + word + '/ids/' + i + '/profile.jpg')
        else:
            imgs.append("")

    print("IMGS:")
    print(imgs)

    return render_template('show_semi.html', id=word, tagList=tags, freqList=freqs, idList=ids,
                           profile='tag_folder/' + word + '/profile/profile.jpg', imgList=imgs)


def chrome_driver_setter():
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


def tag_folder_creater(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return 0
    except:
        return -1


def es_index_creater(word):
    if not es.indices.exists(index=word):
        return es.indices.create(index=word)


def instagram_crawler(ID):
    word = str(ID)
    url = 'https://www.picuki.com/profile/' + word

    # chrome
    # br = webdriver.Chrome()
    br = chrome_driver_setter()
    # br.set_window_size(1500, 1000)

    # br.implicitly_wait(20)
    time.sleep(random.randrange(1, 3))

    suc = False
    count = 3
    while suc != True and count >= 0:
        print(count)
        time.sleep(2)
        count -= 1
        try:
            br.get(url)
            wait = WebDriverWait(br, 10)
            html = br.page_source
            soup = BeautifulSoup(html, 'lxml')
            profile = soup.find('div', 'profile-avatar').find('img')
            post = soup.find('ul', 'box-photos profile-box-photos clearfix').find_all('img')
            suc = True
        except:
            suc = False
            continue

    if suc == False:
        print("failed"*20)
        body = {"tag": "", "freq": -1}
        es.index(index=word, document=body)
        return -1, -1, -1

    doc = {"name": word, "freq": 1}
    es.index(index="id", document=doc)
    # print(id)
    tag_list = []
    human_list = []
    tag_freq = []
    human_freq = []

    tag_folder_creater(f'static/tag_folder/' + word + '/profile')
    imgurl = profile.get("src")
    req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})
    with open(f'static/tag_folder/{word}/profile/profile.jpg', 'wb') as h:
        img = urlopen(req).read()
        h.write(img)

    es_index_creater(word)
    for i in post:
        try:
            list = i.get('alt').split()
            for j in list:
                j = j.replace(',', '')
                if '#' in j:
                    print("#: " + j)
                    if not os.path.exists(f'static/tag_folder/{word}/{j}'):
                        # 각 태그에 해당하는 디렉토리 생성(없을때만)
                        tag_list.append(j)
                        tag_freq.append(1)
                        tag_folder_creater(f'static/tag_folder/' + word + '/' + j)
                        imgurl = i.get("src")
                        req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})

                        # 각 태그에 해당하는 이미지 저장
                        with open(f'static/tag_folder/{word}/{j}/' + 'tagIMG.jpg', 'wb') as h:
                            img = urlopen(req).read()
                            h.write(img)
                            # time.sleep(2)
                    else:
                        tag_freq[tag_list.index(j)] = tag_freq[tag_list.index(j)] + 1

                elif '@' in j:
                    j = j.lower()
                    if j[len(j)-1] == '.':
                        j = j[:len(j)-1]
                    flag = False
                    print("j: "+j)
                    print(human_list)
                    for human in human_list:
                        if j.lower() == human:
                            human_freq[human_list.index(j)] = human_freq[human_list.index(j)] + 1
                            flag = True
                    if not flag:
                        print("@: " + j)
                        human_list.append(j.lower())
                        human_freq.append(1)
        except:
            print("EXCEPT"*20)
            continue

    print(tag_list)
    print(tag_freq)

    if len(tag_list) < 3:
        for i in range(0, 3):
            tag_list.append("")
            tag_freq.append(-1)

    if len(human_list) < 3:
        for i in range(0, 3):
            human_list.append("")
            human_freq.append(-1)

    tag_list, tag_freq = list_alligner(tag_list, tag_freq)
    human_list, human_freq = list_alligner(human_list, human_freq)

    tag_list, tag_freq = list_random_alligner(tag_list, tag_freq)
    human_list, human_freq = list_random_alligner(human_list, human_freq)

    for i in range(0, len(tag_list)):
        body = {"tag": tag_list[i], "freq": tag_freq[i]}
        print(body)
        es.index(index=word, document=body)

    for i in range(0, len(human_list)):
        body = {"tag": human_list[i], "freq": human_freq[i]}
        print(body)
        es.index(index=f'{word}_ids', document=body)

    print(tag_list)
    print(tag_freq)

    print(human_list)
    print(human_freq)

    es_id_crawler(br, word, human_list[0:3])

    # br.close()
    br.quit()

    return tag_list[0:4], tag_freq[0:4], human_list[0:3]

    # 크롤링할 게시물 행 by 열 범위 지정
    # br.execute_script("window.scrollTo(0, 500);")


def es_id_crawler(br, word, ids):
    print("=" * 30 + "idcrawler" + "=" * 30)
    count = 3
    for id in ids:
        suc = False
        while suc != True and count >= 0:
            print(id)
            time.sleep(random.randrange(0, 2))
            count -= 1
            try:
                br.get('https://www.picuki.com/profile/' + id[1:])
                wait = WebDriverWait(br, 10)
                html = br.page_source
                soup = BeautifulSoup(html, 'lxml')
                profile = soup.find('div', 'profile-avatar').find('img')

                tag_folder_creater(f'static/tag_folder/' + word + '/ids/' + id)
                imgurl = profile.get("src")
                req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})
                with open(f'static/tag_folder/{word}/ids/{id}/profile.jpg', 'wb') as h:
                    img = urlopen(req).read()
                    h.write(img)
                suc = True
            except:
                suc = False
                continue
        if suc == False:
            return -1


def list_alligner(sig, freq):
    for i in range(0, len(sig) - 1):
        idx = i
        for j in range(i + 1, len(sig)):
            if freq[j] > freq[idx]:
                idx = j
                print(sig[idx])
                print(sig[i])
        sig[i], sig[idx] = sig[idx], sig[i]
        freq[i], freq[idx] = freq[idx], freq[i]
    print(sig)
    print(freq)
    return sig, freq


def list_random_alligner(sig, freq):
    i = 0
    while i < len(sig):
        top = i
        bottom = i
        randList = []
        tmpList = []
        j = top
        while j < len(sig):
            j += 1
            if j == len(sig):
                return sig, freq
            if freq[j] and freq[i] == freq[j]:
                bottom = j
                break

        if j == len(sig) - 1:
            bottom = len(sig) - 1
        elif freq[top] != freq[top + 1]:
            i += 1
            continue

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
    print(sig)
    print(freq)

    return sig, freq


def es_data_getter(word):
    res = es.search(index=word, size=4)

    dicList = []
    freqList = []
    idList = []
    for i in res['hits']['hits']:
        i = list(i.values())
        dic = list(i[3].values())[0]
        freq = list(i[3].values())[1]
        dicList.append(dic)
        freqList.append(freq)

    print("DICLIST:")
    print(dicList)

    if dicList[0] == "" and freqList[0] == -1:
        if len(dicList) == 1:
            return -1, -1, -1

    res_id = es.search(index=f'{word}_ids', size=3)
    for i in res_id['hits']['hits']:
        i = list(i.values())
        dic = list(i[3].values())[0]
        # freq = list(i[3].values())[1]
        idList.append(dic)
    print(idList)

    return dicList, freqList, idList[0:3]


def es_ids_getter():
    idList = []
    freqList = []

    try:
        res = es.search(index="id", size=10000)
        for i in res['hits']['hits']:
            i = list(i.values())
            id = list(i[3].values())[0]
            freq = list(i[3].values())[1]
            idList.append(id)
            freqList.append(freq)
    except:
        freqList = [0, 0, 0, 0]
        idList = ["", "", "", ""]

    if len(freqList) < 5:
        for i in range(0, 4):
            freqList.append(-1)

    if len(idList) < 5:
        for i in range(0, 4):
            idList.append("")

    idList, freqList = list_alligner(idList, freqList)
    idList, freqList = list_random_alligner(idList, freqList)

    print(idList)
    print(freqList)
    return idList[0:4], freqList[0:4]


def es_freq_counter(word):
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
