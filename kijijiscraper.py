import requests
from lxml import etree
import datetime
import time
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 设置保存路径
path = r'/home/kyber/Pictures/crawler/'
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

def get_img(url):
    headers = {
        "User-Agent": random.choice(user_agent),
        "Referer": "https://www.kijiji.ca/b-cars-trucks/ontario/"
    }
    # 发送请求  获取响应
    response = requests.get(url, headers=headers)
    print('response=', response)

    # response.encoding = 'GBK'
    # print(response.text) # got the html
    html = etree.HTML(response.text)
    
    # try bs4 here
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # bs search for keyword

    img_src = soup.find_all('img', {"data-testid": "listing-card-image"})
    # print('img src parsing result')
    # for item in img_src:
    #     print(item, '\n')
        
     
    print('========================================================')
    key_word = 'media'  # keyword in url to check desired pic

    all_address = []
    all_title = []
  
    for entry in img_src:
        address = entry.get('src')
        title = entry.get('alt')
        if key_word in address:
            print(address)
            address = address.replace("kijijica-200", "kijijica-720")
            print(address)
            all_address.append(address)
            all_title.append(title)


    data_pack = zip(all_address, all_title)

    # print(set(data_pack))


    for img_address, img_desc in data_pack:
        print(img_desc, '\n')
        img_content = requests.get(address, headers=headers).content
        img_name = img_desc[:15] + '.jpg'

        with open(path + img_name, 'wb') as f:  # 图片保存到本地
            print(f"now downloading：{img_name}")
            f.write(img_content)
            f.close()
    time.sleep(random.randint(1, 2))

def main():
    # 要请求的url列表  https://www.kijiji.ca/b-cars-trucks/ontario/page-2 https://www.kijiji.ca/b-cars-trucks/ontario/page-3
    url_list = ['https://www.kijiji.ca/b-cars-trucks/canada/c174l0?sort=dateDesc'] + [f'https://www.kijiji.ca/b-cars-trucks/canada/page-{i}/c174l0?sort=dateDesc' for i in range(2, 1500)]
    # print(url_list)
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(get_img, url_list)
    delta = (datetime.datetime.now() - start).total_seconds()
    print(f"crawling time:{delta}s")


if __name__ == '__main__':
    main()
    