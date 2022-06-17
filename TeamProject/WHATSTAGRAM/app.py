#!usr/bin/python3
# -*- coding: utf-8 -*-

from selenium.webdriver import ActionChains
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
    #return render_template('#')

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

def instagram_crawling():
    # webdriver 설정하기
    app = Flask(__name__)

    # put application's code here
    #word = input("아이디 입력: ")
    word = request.args.get("ID")
    word = str(word)
    url = 'https://www.instagram.com/' + word

    #firefox
    #br = webdriver.Firefox(executable_path=r'./geckodriver')
    #br.get('https://www.instagram.com/')

    #chrome
    #br = webdriver.Chrome()
    br = set_chrome_driver()
    br.set_window_size(1500, 1000)
    br.get('https://www.instagram.com/')
    time.sleep(1.5)

    id_box = br.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input")
    password_box = br.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input")
    login_button = br.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button')

    act = ActionChains(br)

    # 아이디 및 패스워드를 입력 후, 로그인 버튼을 클릭
    act.send_keys_to_element(id_box, 'ospknu@gmail.com').send_keys_to_element(password_box, 'flaskosp').click(
        login_button).perform()
    time.sleep(3)

    # 첫번째 팝업 클릭하기
    # first_popup = br.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')
    # first_popup.click()
    # time.sleep(4)

    # 두번째 팝업 클릭하기

    # second_popup = br.find_element_by_xpath('//*[@id="mount_0_0_fB"]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]')
    # second_popup.click()
    # time.sleep(3)

    # 인스타 사용자의 아이디 url사이트로 넘어가기
    br.get(url)
    time.sleep(10)

    # 해당 페이지의 div 클래스 id를 추출후 # 추가
    html = br.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div')
    id = div['id']
    id = '#' + id

    # print(id)

    tag_list = []
    human_list = []

    # 크롤링할 게시물 행 by 열 범위 지정

    time.sleep(2)
    try:
        #post = br.find_element_by_css_selector(
         #           id + f'> div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div._a3gq > section > main > div > div._aa-i > article > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1) > a > div._aagu > div._aagw')
        post = br.find_element(By.CSS_SELECTOR, id + f'> div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div._a3gq > section > main > div > div._aa-i > article > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1) > a > div._aagu > div._aagw')
        post.click()
        time.sleep(5)
        html = br.page_source
        soup = BeautifulSoup(html, 'lxml')
        print("success")
    except:
        print("fail")
    
    for row in range(1, 4):  # 3 by
        for col in range(1, 4):  # 3
      	   
            print(row,col)
            try:  #게시물이 비었는지 판단하기 위한 try 문 - 오류1해결
               
                post = br.find_element_by_css_selector(
                    id + f'> div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div._a3gq > section > main > div > div._aa-i > article > div:nth-child(1) > div > div:nth-child({row}) > div:nth-child({col}) > a > div._aagu > div._aagw')


                post.click()
                time.sleep(2)
                # css_selector로 format 지정 후 클릭
                html = br.page_source
                soup = BeautifulSoup(html, 'lxml')

                # 태그가 포함된 span 클래스로 접근
                try:
                    #게시물에 글 자체가 없을 때 판단하기 위한 try 문 - 오류2해결
                    tags = soup.find('span', {'class', "_aacl _aaco _aacu _aacx _aad7 _aade"})
                # print(tags)
                    tags = tags.find_all('a')
                    # a 클래스에 태그내용포함되어있음
                    # print(tags)
                    for i in tags:
                        i = i.get_text()
                        if ('#' in i):
                            tag_list.append(i)
                        elif '@' in i:
                            human_list.append(i)
                except:
                    print("글이 없으므로 다음으로 넘어갑니다")

                # a 태그 속 text 추출 및 #으로 태그인지 아닌지 구분
                
                print(tag_list)
                print(human_list)
                # 뒤로 가기
                br.back()

            except:
                print("게시물이 비었습니다")
                



#오류1 : 글 자체가 없으면 findAll() 에러
#오류2 : 게시물 갯수가 적으면 에러
#오류3 : 비공계 처리 어떻게 할건지

if __name__ == "__main__":
    app.run(debug=True)
