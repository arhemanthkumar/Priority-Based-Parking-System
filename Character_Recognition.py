# To detect time-stamps from the bottom left of the image.
import cv2
import thresh
from PIL import Image
from pytesseract import pytesseract
import os
# global date
date = ""
# date = ""
# global time
time = ""

# img_name = "TC_00057.jpg"

def get_date_and_time(img_name):
    path_to_tesseract = r'/usr/bin/tesseract'
    # custom config for tesseract whitelist = r'/usr/share/tesseract-ocr/4.00/tessdata/configs/custom.txt'
    # print(img_name)

    # img_name = os.getcwd() + "/input_images/" + img_name
    pytesseract.tesseract_cmd = path_to_tesseract

    img = Image.open(img_name)
    # img.show()

    # "date" and "time" are assumed to be at the bottom left of the image
    # Assuming the image size is 800x600
    # Coordinates: (left, top, right, bottom)
    box = (0, 600 - 37, 300, 600)
    img2 = img.crop(box)

    croppedImage = "cropped_image.png"
    img2.save(croppedImage)
    # img2.show()

    img3 = Image.open(croppedImage)

    text = pytesseract.image_to_string(img3)
    # print(text)
    # print(type(text))
    index_of_last_char = text.index("M")
    comma = text.index(",")
    global date
    date = text[:comma]
    # print("Date : ", date)
    global time
    time = text[comma + 2 : index_of_last_char+1]
    # print("Time : ", time)
    return date, time


def get_license_plate_info(name_of_image, x_recieved, y_recieved, width_recieved, height_recieved):
    image = cv2.imread(name_of_image, 0)
    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # co-ordinates have to be extracted in bounding boxes from main.py file
    # x, y, w, h = 207, 217, 455, 97
    # x_recieved = 207
    # y_recieved = 217
    # width_recieved = 455
    # height_recieved = 97

    x, y, w, h = x_recieved + 10, y_recieved + 10, width_recieved - 10, height_recieved - 10
    ROI = thresh[y:y + h, x:x + w]
    data = pytesseract.image_to_string(ROI, lang='LicensePlate', config='--psm 6 /usr/share/tesseract-ocr/4.00/tessdata/configs/custom.txt').upper()

    # print(data)     # It displays data in multiline format, for eg., it prints 2 lines if license plate has 2 lines
    list_of_data = list(data)    # We convert that 2 list
    # print(list_of_data)
    modified_data = ""      # We convert that multiline data into single line by replacing characteres such as "\n" and "\x0c"
    for char in list_of_data:
        if char == "\n" or char == "\x0c":
            continue
        modified_data += char
    # print(modified_data)        # We print the modified data in a asingle line
    # print(len(data))
    # cv2.imshow('thresh', thresh)  #entire image with threshold applied
    # cv2.imshow('ROI', ROI)  #number_plate with threshold applied and cropped
    cv2.waitKey(0)
    return modified_data

# print(os.getcwd())

if __name__ == '__main__':
    get_date_and_time(img_name)
    get_license_plate_info(img_name)
    # get_license_plate_info(img_name, 207, 217, 455, 97)


def fetch_date_and_time():
    accessable_date = date
    accessable_time = time
    return accessable_date, accessable_time