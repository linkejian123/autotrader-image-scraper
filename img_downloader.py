
import requests
import random
import time
import re
from lxml import etree
from bs4 import BeautifulSoup
import os
import csv
# test save catche
# url = 'https://3dmodels.org/360-view/?id=235798'
# 设置保存路径
list_path = r'/home/val/Pictures/crawler2/url_list.csv'
dl_path = r'/home/val/Pictures/crawler2/'
progress_path = r'/home/val/Pictures/crawler2/checker.txt'




def dl_img(url_list, car_path):
    for url in url_list:
        try:
            print('DDDDDDDDDDDDDDDDDDDDDDDDDD')
            print(url)
            # Send an HTTP GET request to the URL
            time.sleep(random.randint(1, 2))
            response = requests.get(url)
            response.raise_for_status()  # Check for any errors in the response

            # Extract the image data
            image_data = response.content

            img_name = url.split("-")[-1]

            # Specify the file path within the folder using the extracted file name
            file_path = os.path.join(car_path, img_name)

            # Open the file in binary write mode and save the image data
            with open(file_path, "wb") as file:
                file.write(image_data)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image for {title}: {e}")
            



def strip_imgurl(title, url):
    # Create a folder with the title as its name
    car_path = os.path.join(dl_path, title)
    os.makedirs(car_path, exist_ok=True)
    
    try:
        page360 = requests.get(url, headers=headers)
        
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
                # print(javascript_code)

        preload_pattern = re.compile(r'preload\(\[([\s\S]*?)\]\);')
        match = preload_pattern.search(javascript_code)

        if match:
            preload_matrix_text = match.group(1).strip()  # Extract the content of the matrix
            # Split the matrix into individual URLs
            url_list = preload_matrix_text.split(',')
            # Remove quotation marks from each URL
            url_list = [url.replace('"', '').replace("'", '').replace('\n', '').replace('\t', '') for url in url_list]
            dl_img(url_list, car_path)
            print(url_list)
        else:
            print("ERROR!! No preload matrix found in the JavaScript code.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image for {title}: {e}")
        
# Create the parent directory if it doesn't exist
os.makedirs(dl_path, exist_ok=True)


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

# Open the file in read mode
row_to_read = 1  # Adjust as needed


# Read the last processed line number from the progress file
try:
    with open(progress_path, 'r') as pf:
        last_processed_line = int(pf.readline().strip())
except FileNotFoundError:
    last_processed_line = 0
# Determine whether to start from the beginning or resume
if last_processed_line <= 0:
    print(f"Starting from the beginning for file: {list_path}")
else:
    print(f"Resuming from line {last_processed_line} for file: {list_path}")
# Open the CSV file and process each row
with open(list_path, 'r', newline='') as file:
    reader = csv.reader(file)
    
    for line_num, row in enumerate(reader, start=1):
        if line_num <= last_processed_line:
            continue  # Skip rows that have already been processed
        
        # Perform your processing on the row here
        serial, status, title, url = row
        strip_imgurl(title, url)
        
        # Update the progress file with the current line number
        with open(progress_path, 'w') as pf:
            pf.write(str(line_num))


