from pdf2image import convert_from_path
import cv2
import os
import numpy as np
import pytesseract as tess
from PIL import Image
from textblob import TextBlob
import concurrent.futures
import multiprocessing
import time

# the line below can be commented out if you have tesseract added to your PATH. If not, then include the line below.
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
start = time.time()

dpath = r"C:\Users\Shubhankar\Desktop\PDF_Text_Recognition\temp"


# l = os.listdir(dpath)  # dpath is your directory path
# number_files = len(l)

# path_pdf = r'D:\Projects\Projects\Dell hackathon\OCR_V1\pdfs\wordpress-pdf-invoice-plugin-sample.pdf '
# path_pdf = r'D:\Projects\Projects\Dell hackathon\OCR_V1\pdfs\Invoice_TM-0005(signed).pdf'
# path_pdf = r'C:\Users\Shubhankar\Desktop\PDF_Text_Recognition\test_files\test3.pdf'


# gives coordinates of text boxes
def coordinates(arr):
    max_x = int(np.amax(arr, axis=0)[0][0])
    max_y = int(np.amax(arr, axis=0)[0][1])
    min_x = int(np.amin(arr, axis=0)[0][0])
    min_y = int(np.amin(arr, axis=0)[0][1])

    return min_x, min_y, max_x, max_y


# extracts texts from image
def Image2Text(img):
    img_txt = ''
    gap = "\n"
    resize_val = 2000
    kernel_size = 9
    (h, w, d) = img.shape

    # ---------------------------------------Image Preprocessing-------------------------------------

    # resizing the image to reduce size
    r = resize_val / w
    dim = (resize_val, int(h * r))
    resized = cv2.resize(img, dim)
    temp = resized
    img = temp

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilate = cv2.dilate(edged, kernel, iterations=4)

    # -----------------------Contour detection-----------------------------------------------------
    cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    len1 = len(cnts)

    # counter1 = 0
    # for i in cnts:
    #     x1,y1,x2,y2 = coordinates(cnts[counter1])
    #     counter1 += 1

    i = 0
    new_gray = gray
    # ------------------------------extraction of contours and then text-----------------------------------
    while i < len1:
        x1, y1, x2, y2 = coordinates(cnts[i])
        cropped = new_gray[y1:y2, x1:x2]  # a text concentrated section of the cropped
        bright = cv2.inRange(cropped, 150, 255)

        pil_image = Image.fromarray(bright)
        text = tess.image_to_string(pil_image, config='--psm 6')  # text is extracted from the cropped section only
        img_txt = img_txt + text + gap

        new_gray[y1:y2, x1:x2] = 255
        i += 1
    # img_txt = img_txt.replace('-\n', '')
    return img_txt


# ------------------------------------------------pdf to jpg---------------------------------

def execute(path_pdf, name):
    pages = convert_from_path(path_pdf, 450, fmt='png')  # converts pdf into set of images
    count = 0
    content = ''
    for page in pages:
        count += 1
        pil_image = page
        open_cv_image = np.array(pil_image)
        image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # -------------------------------------------getting text from image------------------------

        document_text = Image2Text(image)
        corrected_document_text = TextBlob(document_text)  # spellchecker

        content = content + str(corrected_document_text)

    # -----------------------------------------------saving it in a text file------------------------------
    name = name.replace('.pdf', '.txt')
    # print(name)
    text_file_path = r'C:\Users\Shubhankar\Desktop\PDF_Text_Recognition\extracted' + "\\" + name
    text_file = open(text_file_path, "w")
    text_file.write(content)
    text_file.close()
    # os.remove(path_pdf)


# execute(r'C:\Users\Shubhankar\Desktop\PDF_Text_Recognition\test_files\test3.pdf')


# for filename in os.listdir(dpath):
#     filepath = dpath + '\\' + filename
#     execute(filepath, filename)
#
# end = time.time()
# print("time elapsed: " + str(end - start))


# with concurrent.futures.ProcessPoolExecutor() as executor:
#     if __name__ == '__main__':
#         for filename in os.listdir(dpath):
#             filepath = dpath + '\\' + filename
#             executor.submit(execute, filepath, filename)
#             # print(filepath)


if __name__ == '__main__':
    processes = []
    for filename in os.listdir(dpath):
        filepath = dpath + '\\' + filename
        p = multiprocessing.Process(target=execute, args=(filepath, filename))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()
    end = time.time()
    print("time elapsed: " + str(end - start))


