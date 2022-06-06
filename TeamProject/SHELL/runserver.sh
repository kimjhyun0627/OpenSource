#!/usr/bin/bash

read -p "apt-get update를 위한 사용자 패스워드를 입력해주세요 : " PW

echo "$PW" | sudo -kS apt-get update
#echo "$PW" | sudo -kS apt install software-properties-common
#echo "$PW" | sudo -kS apt install python3.9
python3 --version
#echo "$PW" | sudo -kS apt install python3-pip build-essential

#echo "$PW" | sudo -kS apt-get update
#echo "$PW" | sudo -kS apt-get upgrade -y

#echo "$PW" | pip install flask
#echo "$PW" | sudo -kS apt-get install python3-bs4

#echo "$PW" | sudo -kS apt-get update

chmod 700 runelasticsearch.sh
chmod 700 runbrowser.sh

#./runelasticsearch.sh

gnome-terminal -e ./runelasticsearch.sh
gnome-terminal -e ./runbrowser.sh

python3 app.py