#!/usr/bin/bash

read -p "password : " PW

echo "$PW" | sudo -kS apt-get update
echo "$PW" | sudo -kS apt install software-properties-common
echo "$PW" | sudo -kS apt install python3.9
python3 --version
echo "$PW" | sudo -kS apt install python3-pip build-essesioal

echo "$PW" | sudo -kS apt-get update
echo "$PW" | sudo -kS apt-get upgrade -y

echo "$PW" | pip install flask
echo "$PW" | sudo -kS apt-get install python3-bs4

echo "$PW" | sudo -kS apt-get update

chmod 700 runelasticsearch.sh
./runelasticsearch.sh

python3 app.py