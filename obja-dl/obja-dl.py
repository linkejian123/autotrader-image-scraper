import os
import objaverse
import json
import io
from tqdm import tqdm
import ssl
import trimesh
import multiprocessing
import requests
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
ssl._create_default_https_context = ssl._create_unverified_context

def check_img(uid, img_url, uid_file:io.TextIOWrapper):
    def on_press(event):
        if event.key == 'k':
            uid_file.write(uid + '\n')
            uid_file.flush()
            print(uid, "added")
            plt.close()
        elif event.key == 'l':
            print(uid, "discarded")
            plt.close()
            return
        else:
            print("Wrong key. Please retry.")
    try:
        response = requests.get(img_url)
        img = Image.open(io.BytesIO(response.content))
        fig, ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', on_press)
        ax.imshow(img)
        ax.set_title("Press k to add or press l to discard")
        plt.show()
    except:
        print("Error reading image: uid", uid, "url", img_url)

if __name__ == '__main__':
    uids = objaverse.load_uids()
    annotations = objaverse.load_annotations(uids)
    car_annotations = {}
    for uid in annotations:
        tags = annotations[uid]['tags']
        for tag in tags:
            if tag['name'] == 'honda':
                car_annotations[uid] = annotations[uid]
                break
    print(len(car_annotations))
    car_uids_f = open("car_uids.txt", "w")
    for car_uid in car_annotations:
        images_meta = car_annotations[car_uid]['thumbnails']['images']
        max_size = 0
        max_idx = 0
        for i, img_meta in enumerate(images_meta):
            img_size = img_meta["width"] * img_meta["height"]
            if img_size > max_size:
                max_idx = i
                max_size = img_size
        url = images_meta[max_idx]["url"]
        check_img(car_uid, url, car_uids_f)
    car_uids_f.close()
