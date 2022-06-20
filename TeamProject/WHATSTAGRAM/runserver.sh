#!/bin/bash

read -p "슈퍼유저 명령 처리를 위한 사용자 패스워드를 입력해주세요 : " PW

echo "$PW" | sudo -kS apt-get update
python3 --version
echo "$PW" | sudo -kS pip install -r requirements.txt
pip install -U selenium
pip install lxml

chmod 700 runelasticsearch.sh
chmod 700 runbrowser.sh

#./runelasticsearch.sh
gnome-terminal -e ./runelasticsearch.sh

# 설치파일 받기 -> 나중에 살리기
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 크롬 설치 -> 나중에 살리기
echo "$PW" | sudo -kS apt install ./google-chrome-stable_current_amd64.deb

# 크롬 버전 확인
google-chrome --version


echo "$PW" | sudo -kS apt install software-properties-common
echo "$PW" | sudo -kS apt install python3.9

echo "$PW" | sudo -kS apt install python3-pip build-essential

pip install webdriver-manager
pip install requests
pip install beautifulsoup4
pip install konlpy
pip install datetime

#echo "$PW" | sudo -kS apt-get update
#echo "$PW" | sudo -kS apt-get upgrade -y

#pip install flask
#echo "$PW" | sudo -kS apt-get install python3-bs4

echo "$PW" | sudo -kS apt-get update

#echo "$PW" | pip install flask
#echo "$PW" | sudo -kS apt-get install python3-bs4

#echo "$PW" | sudo -kS apt-get update

#testbigbrother

gnome-terminal -e ./runbrowser.sh

python3 app.py
