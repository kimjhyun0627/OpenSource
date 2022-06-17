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


@app.route('/', methods=['GET'])
def home():
    return render_template('main.html')


@app.route('/view', methods=['GET'])
def crawl():
    instagram_crawling()
    # return render_template('#')


# @app.route('/crawl', methods=['GET', 'POST'])
# def dosomething():
#     # TODO: 내용 넣기
#     return

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def create_tagfolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except:
        return


def instagram_crawling():
    # webdriver 설정하기
    app = Flask(__name__)

    # put application's code here
    # word = input("아이디 입력: ")
    word = request.args.get("ID")
    create_tagfolder('static/tag_folder/')
    create_tagfolder('static/tag_folder/' + word)
    word = str(word)
    url = 'https://www.picuki.com/profile/' + word

    # chrome
    # br = webdriver.Chrome()
    br = set_chrome_driver()
    br.set_window_size(1500, 1000)
    br.get(url)
    time.sleep(4)

    # 해당 페이지의 div 클래스 id를 추출후 # 추가
    html = br.page_source
    soup = BeautifulSoup(html, 'lxml')
    profile = soup.find('div', 'profile-avatar').find('img')
    post = soup.find('ul', 'box-photos profile-box-photos clearfix').find_all('img')

    # print(id)
    list = []
    tag_list = []
    human_list = []
    br.close()

    create_tagfolder(f'static/tag_folder/' + word + '/profile')
    imgurl = profile.get("src")
    req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})
    with open(f'static/tag_folder/{word}/profile/profile.jpg', 'wb') as h:
        img = urlopen(req).read()
        h.write(img)

    n = 1
    for i in post:
        try:
            list = i.get('alt').split()
            print(list)
            for j in list:
                if '#' in j:
                    if not os.path.exists(f'static/tag_folder/{word}/{j}'):
                        # 각 태그에 해당하는 디렉토리 생성(없을때만)
                        tag_list.append(j)
                        create_tagfolder(f'static/tag_folder/' + word + '/' + j)
                        imgurl = i.get("src")
                        req = Request(imgurl, headers={'User-Agent': 'Mozilla/5.0'})

                        # 각 태그에 해당하는 이미지 저장
                        with open(f'static/tag_folder/{word}/{j}/' + str(n) + '.jpg', 'wb') as h:
                            img = urlopen(req).read()
                            h.write(img)
                            n = n + 1

                elif '@' in j:
                    human_list.append(j)
        except:
            continue
        #print(i.get("src"))
        print("=" * 20)
        list = []

    print(tag_list)
    print(human_list)

    # 크롤링할 게시물 행 by 열 범위 지정
    # br.execute_script("window.scrollTo(0, 500);")
    time.sleep(5)


# 오류1 : 글 자체가 없으면 findAll() 에러
# 오류2 : 게시물 갯수가 적으면 에러
# 오류3 : 비공계 처리 어떻게 할건지

if __name__ == "__main__":
    app.run(debug=True)
