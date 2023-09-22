import requests
from lxml import etree
import datetime
import time
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

path = r'/home/kyber/Pictures/crawler/'
headers = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
list = {('https://media.kijiji.ca/api/v1/autos-prod-ads/images/03/03a27501-e889-490d-8da5-3646a75134df?rule=kijijica-200-jpg', '2018 Honda Civic Touring - Heated F+R seats, Leather, Sunroof, A'), ('https://media.kijiji.ca/api/v1/autos-prod-ads/images/c3/c3dd84e1-fc1d-474c-a0e3-a1aa289c618b?rule=kijijica-200-jpg', ' 2021 Ram 1500 Classic SLT 5.7L'), ('https://media.kijiji.ca/api/v1/autos-prod-ads/images/b6/b689d121-8ddc-4b7f-9b4e-645d15b52382?rule=kijijica-200-jpg', '2010 Mercedes-Benz B-Class B 200'), ('https://media.kijiji.ca/api/v1/autos-prod-ads/images/6e/6e6978d4-8af8-4fd7-8d12-53a9c452ce3c?rule=kijijica-200-jpg', '2021 Dodge Challenger GT Blacktop | AWD | Leather | Sunroof'), ('https://media.kijiji.ca/api/v1/ca-prod-fsbo-ads/images/99/99d32944-af13-4cf6-960d-f20a3c55a509?rule=kijijica-200-jpg', 'Ford Focus 2015   AUTO, AC, Backup Cam, Bluetooth,Certifie')}

for img_address, img_desc in list:
        print(img_address, '\n')
        img_content = requests.get(img_address, headers).content
        img_name = img_desc[:10] + '.jpg'

        with open(path + img_name, 'wb') as f:  # 图片保存到本地
            print(f"now downloading：{img_name}")
            f.write(img_content)
            f.close()
time.sleep(random.randint(1, 2))