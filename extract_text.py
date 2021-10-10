
from PIL import Image
import pytesseract
import time
import sys
import cv2
from pdf2image import convert_from_path
import os
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

start_time = time.time()

DIRECTORY_PATH = r'C:\Users\Shubhankar\Desktop\PDF_Text_Recognition'
PDF_PATH = DIRECTORY_PATH + r'\test_files\test3.pdf'
PAGES = convert_from_path(PDF_PATH, 500)

i = 0
for p in PAGES:
    img_name = r'img_temp\Page_' + str(i) + '.jpg'
    p.save(img_name, "JPEG")
    i = i + 1

j = 0

string = ''

while j < i:

    img = Image.open(DIRECTORY_PATH + r'\img_temp\Page_' + str(j) + '.jpg')
    string += pytesseract.image_to_string(img, lang='eng')
    string += '\n\n'

    if os.path.exists(DIRECTORY_PATH + r'\img_temp\Page_' + str(j) + '.jpg'):
        os.remove(DIRECTORY_PATH + r'\img_temp\Page_' + str(j) + '.jpg')
    else:
        print("The file does not exist")

    j = j + 1

string = string.replace('-\n', '')


txt_file = open(DIRECTORY_PATH + r'\extracted\data.txt', 'w')
txt_file.write(string)
txt_file.close()

print("--- %s seconds ---" % (time.time() - start_time))









