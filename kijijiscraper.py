import requests
from lxml import etree
import datetime
import time
import random
from concurrent.futures import ThreadPoolExecutor

# 设置保存路径
path = r'/home/val/Pictures/crawler/ '
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
    # 打印网页源代码来看  乱码   重新设置编码解决编码问题
    # 内容正常显示  便于之后提取数据
    response.encoding = 'GBK'
    html = etree.HTML(response.text)
    # print(html.text) # kijiji got 200 
    
    # xpath定位提取想要的数据  得到图片链接和名称
    # img_src = html.xpath('//ul[@class="clearfix"]/li/a/img/@src')
    img_src = html.xpath('//li[@data-testid=""]')
    print('img src parsing result', img_src)
    
    # edit imgsrc to get true url to pic
    # img_src = ['http://pic.netbian.com' + x for x in img_src]
    img_alt = html.xpath('//ul[@class="clearfix"]/li/a/img/@alt') # alt to get name
    for src, name in zip(img_src, img_alt):
        img_content = requests.get(src, headers=headers).content
        img_name = name + '.jpg'
        with open(path + img_name, 'wb') as f:  # 图片保存到本地
            print(f"now downloading：{img_name}")
            f.close()
            # f.write(img_content)
    time.sleep(random.randint(1, 2))

def main():
    # 要请求的url列表  https://www.kijiji.ca/b-cars-trucks/ontario/page-2 https://www.kijiji.ca/b-cars-trucks/ontario/page-3
    url_list = ['https://www.kijiji.ca/b-cars-trucks/canada/c174l0?sort=dateDesc'] + [f'https://www.kijiji.ca/b-cars-trucks/canada/page-{i}/c174l0?sort=dateDesc' for i in range(2, 4)]
    print(url_list)
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(get_img, url_list)
    delta = (datetime.datetime.now() - start).total_seconds()
    print(f"craling time:{delta}s")

if __name__ == '__main__':
    main()