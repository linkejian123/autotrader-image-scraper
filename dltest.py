
import requests
import random
import re
from lxml import etree
from bs4 import BeautifulSoup
import os
# test save catche
url = 'https://3dmodels.org/360-view/?id=235798'
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
headers = {
        "User-Agent": random.choice(user_agent),
        "Referer": "https://3dmodels.org/3d-models/lexus-tx-premium-us-spec-2023"
    }
page360 = requests.get(url, headers=headers)
html = etree.HTML(page360.text)

    
# try bs4 here
soup = BeautifulSoup(page360.content, 'html.parser')

script_tags = soup.find_all('script')

# Search for the script containing 'preload' matrix
for script_tag in script_tags:
    if 'preload' in script_tag.text:
        # Extract the JavaScript content
        javascript_code = script_tag.text
        
        # Now, you can work with the JavaScript code to extract the 'preload' matrix
        # You may use regular expressions or other parsing techniques

        # For demonstration, let's print the entire JavaScript code:
        print(javascript_code)

preload_pattern = re.compile(r'preload\(\[([\s\S]*?)\]\);')
match = preload_pattern.search(javascript_code)

if match:
    preload_matrix_text = match.group(1).strip()  # Extract the content of the matrix
    # Split the matrix into individual URLs
    url_list = preload_matrix_text.split(',')
    # Optionally, you can further clean up the URLs, remove leading/trailing spaces, etc.
    url_list = [url.strip() for url in url_list]
    print(url_list)
else:
    print("No preload matrix found in the JavaScript code.")
