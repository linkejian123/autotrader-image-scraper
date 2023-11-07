
import requests
import random
import re
from lxml import etree
from bs4 import BeautifulSoup
import os
# test save catche
# url = 'https://3dmodels.org/360-view/?id=235798'
# 设置保存路径
list_path = r'/home/val/Pictures/crawler2/list.txt'
full_list = {}  # initialize full url dict
dl_path = r'/home/val/Pictures/crawler2/'

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
if os.path.exists(list_path):
    with open(list_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
             # Split each line by the comma and strip whitespace
            values = [value.strip() for value in line.split(',')]

            # Check if there are at least 2 values
            if len(values) >= 2:
                key, value = values[0], values[1]
                # Add the key-value pair to the dictionary
                full_list[key] = value
            else:
                print(f"Ignored line with insufficient values: {line.strip()}")

    # Close the file
    file.close()
else:
    print("LIST FILE DOES NOT EXIST")


def dl_img(url_list, car_path):
    for url in url_list:
        try:
            print('DDDDDDDDDDDDDDDDDDDDDDDDDD')
            # Send an HTTP GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Check for any errors in the response

            # Extract the image data
            image_data = response.content

            img_name = url.split("/")[-1]

            # Specify the file path within the folder using the extracted file name
            file_path = os.path.join(car_path, img_name)

            # Open the file in binary write mode and save the image data
            with open(file_path, "wb") as file:
                file.write(image_data)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image for {title}: {e}")
            

for title, url in full_list.items(): 
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
            url_list = [url.strip('"') for url in url_list]
            dl_img(url_list, car_path)
            print(url_list)
        else:
            print("ERROR!! No preload matrix found in the JavaScript code.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image for {title}: {e}")
        
        
