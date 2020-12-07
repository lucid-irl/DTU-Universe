from pytesseract.pytesseract import main
import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import cv2


def get_captcha_id() -> str:
    html = requests.get('https://mydtu.duytan.edu.vn/Signin.aspx').text
    captcha_div = BeautifulSoup(html, 'lxml').find(id='box-captcha')
    img = captcha_div.find('img')
    return str(img['src']).split('=')[1]

def download_captcha_image(id: str, folder: str):
    file_name = folder+'\\'+id+'.jpeg'
    url = 'https://mydtu.duytan.edu.vn/CaptchaImage.axd?guid={}'.format(id)
    urlretrieve(url, filename=file_name)

def convert_to_binary(img_grayscale, thresh=100):
    thresh, img_binary = cv2.threshold(img_grayscale, thresh, maxval=255, type=cv2.THRESH_BINARY)
    return img_binary

def grayscale_image(path):
    img_grayscale = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img_grayscale

def convert_to_binary_use_adaptive_threshold(img_grayscale):
    img_binary = cv2.adaptiveThreshold(img_grayscale, 
                                       maxValue=255, 
                                       adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, 
                                       thresholdType=cv2.THRESH_BINARY,
                                       blockSize=15,
                                       C=8)
    return img_binary

def remove_noise_opencv(filename):
    img = cv2.imread(filename)
    dst = cv2.fastNlMeansDenoisingColored(img,None,12,12,7,21)
    return dst


def cut_image_and_move_to_folders(image_file_name: str, folder: str):
    image_file_name

if __name__ == "__main__":
    file_name = 'characters\\img1__0ef43542-f90d-4d32-a6d1-bd14db35dfae.jpeg'
    im = remove_noise_opencv(file_name)
    im = convert_to_binary(im)
    cv2.imshow('ok',im)
    cv2.waitKey(0)