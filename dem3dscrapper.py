import requests
from lxml import etree
import datetime
import time
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

import os  # libs needed for car filtration
import sys
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt
from openvino.runtime import Core

sys.path.append("../utils")
import notebook_utils as utils


# 设置保存路径
path = r'/home/kyber/Pictures/crawler2/'
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
start = datetime.datetime.now()

def check360(son_url):  # checked with ground truth, it works

    headers = {
        "User-Agent": random.choice(user_agent),
        "Referer": "https://3dmodels.org/3d-models/vehicles/"
    }
    # 发送请求  获取响应
    response = requests.get(son_url, headers=headers)  
    # print('son_response=', response)

    # response.encoding = 'GBK'
    # print(response.text) # got the html
    html = etree.HTML(response.text)
    
    # try bs4 here
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find_all('li', {"class": "launcher-360"})
    if result:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        return True
    else:
        # print('no 360')
        return False
    
    
    


def get_img(url):
    headers = {
        "User-Agent": random.choice(user_agent),
        "Referer": "https://3dmodels.org/3d-models/vehicles/"
    }
    # 发送请求  获取响应
    response = requests.get(url, headers=headers)
    # print('response=', response)

    # response.encoding = 'GBK'
    # print(response.text) # got the html
    html = etree.HTML(response.text)
    
    # try bs4 here
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # bs search for keyword

    son_page_list = soup.find_all('a', {"class": "img-full-prod lt pos_rel fwidth over_hid"})
    # print(son_page_list)
    
    print('========================================================')
    key_word = '/#360view'  # keyword in url to check desired pic

    all_address = []
    all_title = []
    counter = 0

    for entry in son_page_list:
        counter +=1 
        son_address = entry.get('href')
        
        title = entry.get('title')
        print(counter, title)

        # print(son_address)
        
        checker = check360(son_address)
        if checker is True:
            print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            print(title)
            print('YYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
            son_address360 = son_address + '/#360view'
            
            save_img(son_address360)
            
            
        else:
            continue

    print('FFFFFFFFFFFFFFFFFf')

def save_img(url):
    print(url)


    # for img_address, img_desc in data_pack:
        # print(img_desc, '\n')
        # img_content = requests.get(son_address, headers=headers).content
        # img_name = img_desc[:20] + '.jpg'
# 
        # with open(path + img_name, 'wb') as f:  # 图片保存到本地
            # print(f"now downloading：{img_name}")
            # f.write(img_content)
            # f.close()
    time.sleep(random.randint(1, 2))



def main():


    # 要请求的url列表  https://3dmodels.org/3d-models/vehicles/page/2/
    url_list = ['https://3dmodels.org/3d-models/vehicles/'] + [f'https://3dmodels.org/3d-models/vehicles/page/{i}/' for i in range(2, 5)]
    # print(url_list)
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(get_img, url_list)
    delta = (datetime.datetime.now() - start).total_seconds()
    print(f"crawling time:{delta}s")


if __name__ == '__main__':
    main()
    