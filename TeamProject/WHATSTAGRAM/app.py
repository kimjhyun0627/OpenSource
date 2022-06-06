#!usr/bin/python3
# -*- coding: utf-8 -*-

import re
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
es_host = "http://localhost:9200"

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html')

@app.route('/crawl', methods=['GET', 'POST'])
def dosomething():
    # TODO: 내용 넣기
    return

if __name__ == "__main__":
    app.run(debug=True)