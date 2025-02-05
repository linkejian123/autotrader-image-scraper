#!/usr/bin/env python
import os
import threading

import queue
import requests
from bs4 import BeautifulSoup

DOMAIN = 'http://www.autotrader.ca'
START_URL = DOMAIN + '/cars'
CONTENT_ROOT = '/home/val/Pictures/crawler/'


def do_work(data):
    directory = os.path.join(CONTENT_ROOT,data.get('slug'))
    if not os.path.exists(directory):
        os.mkdir(directory)
    url = data.get('url')
    filename = url.split('/').pop()
    try:
        r = requests.get(url, stream=True)
        print('request got')
    except:
        print('Skipped image %s' % url)
        return

    if r.status_code == 200:
        with open(directory + '/'+ filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)        

def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = queue.Queue()

for i in range(4):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()

def item_page(url, slug, year):
    try:
        r = requests.get(url)    
    except:
        print('Skipped item %s' % url)
        return

    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all('a'):

        img = a.get('data-rsbigimg')
        if img:
            href = a.get('href')
            data = {
                'url':href,
                'slug':slug,
                'year': year
            }
            print(data)
            q.put(data)
            break


def overview_page(start=0, end=1):
    for i in range(start, end):
        params = {}
        if i > 0:
            params['search'] = i + 1

        try:
            r = requests.get(START_URL, params=params)
            print(START_URL)
            
        except:
            print('Skipped page %s' % (i+1))
            continue
        soup = BeautifulSoup(r.text, "lxml")
        print(r.text)

        for section in soup.find_all('section'):
            classes = section.get('class')

            if classes and 'result' in classes:
                title_element = section.find_all('h2')[0]
                href = title_element.a.get('href')

                parts = href.split('/')
                slug = parts[2]
                year = parts[3]
                url = DOMAIN + href
                item_page(url, slug, year)
                print(slug, year)#, url

        print('============= PAGE %s =============' % (i + 1))
    
if __name__ == '__main__':
    if not os.path.exists(CONTENT_ROOT):
        os.mkdir(CONTENT_ROOT)
    overview_page(start=1, end=4)
    q.join()
    print('ok')