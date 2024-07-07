import cv2  # imports cv2 module for image manipulation and image processing
import thresh  # imports thresh to apply filters and threshold to the images
from PIL import Image  # imports Image from PIL to open, save and close various formats of images
from pytesseract import pytesseract  # imports pytesseract for character recognition
import os

date = ""  # to store date from the image
time = ""  # to store time from the image


# img_name = "img68", in-case, running the program alone, give any image name available from inside input_images folder

def get_date_and_time(img_name):  # to detect and read, date and time from the image
    path_to_tesseract = r'/usr/bin/tesseract'  # mention the path of the tesseract, so that the compiler calls pytesseract from the installed directory

    '''
    # custom config for tesseract whitelist = r'/usr/share/tesseract-ocr/4.00/tessdata/configs/custom.txt'
    So, a test case to handle is that, pytesseract is not perfect
    License Plate contains characters such as alphabets and numbers only
    There is a chance of pytesseract reading other characters such as special characters like %, $, *, (, ", !, }, -,..
    This have to be avoided to ensure better accuracy
    So, we have to create a config file for tesseract and name it custom.txt in the path specified above
    Inside white list the charcters "ABCDEFGHIJKMNOPQRSTUVWXYZ1234567890", so that only these characters are allowed
    
    The custom.txt file contains:
    Line 1. - load_system_dawg false
    Line 2. - load_freq_dawg false
    Line 3. - tessedit_char_whitelist ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
    '''

    # print(img_name)

    pytesseract.tesseract_cmd = path_to_tesseract  # we specify the tesseract compiler to look for the tesseract in this directory

    img = Image.open(img_name)  # we open the image by its name
    # img.show()

    # "date" and "time" are assumed to be at the bottom left of the image
    # Assuming the image size is 800x600
    # Coordinates: (left, top, right, bottom)
    box = (0, 600 - 37, 300, 600)  # co-ordinates are fixed for the file size
    img2 = img.crop(box)  # we crop the image which contains date and time at te bottom left

    croppedImage = "cropped_image.png"  # we give the name of the cropped image as cropped_image
    img2.save(croppedImage)  # we will save this and pass this to tesseract to read date and time
    # img2.show()

    img3 = Image.open(croppedImage)  # we open the cropped image which was saved earlier

    text = pytesseract.image_to_string(img3)  # we call tesseract method image_to_string to convert the image which contains date and time into text or in the form of string
    # print(text)
    # print(type(text))
    # sample looks like this: 20/06/24, 11:42 AM as a single string, we need to seperate date and time
    index_of_last_char = text.index("M")  # So, the date and time string ends with time specifically, with AM or PM, so we get index of last element
    comma = text.index(",")  # we get the index of comma(,)
    global date  # we declare date as global to access it outside the function and to pass it to other modules
    date = text[:comma]  # we extract date from splicing the string from beginning till the comma which gives us the date
    # print("Date : ", date)
    global time  # we declare time as global to access it outside the function and to pass it to other modules
    time = text[comma + 2: index_of_last_char + 1]  # we extract time from comma till the last charater M
    # print("Time : ", time)
    return date, time  # we return the date and time


# get_license_plate_info function reads the name of the image and the co-ordinates of the bounding boxes of the number plate detected from yolo in main.py
def get_license_plate_info(name_of_image, x_recieved, y_recieved, width_recieved, height_recieved):
    image = cv2.imread(name_of_image, 0)  # opens the image for processing
    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # cv2.THRESH_OTSU finds the optimal threshold value combined with cv2.THRESH_BINARY_INV inverts the binary threshold
    # the minimum value of threshold being 0 and maximum value of threshold being 255

    # co-ordinates have to be extracted in bounding boxes from main.py file
    # x, y, w, h = 207, 217, 455, 97
    # x_recieved = 207
    # y_recieved = 217
    # width_recieved = 455
    # height_recieved = 97
    # While running, standalone program, enable the above c-ordinates for img50
    x, y, w, h = x_recieved + 10, y_recieved + 10, width_recieved - 10, height_recieved - 10
    # cropping the bounding boxes value by another 10 pixels for accuracy
    ROI = thresh[y:y + h, x:x + w]  # Region of Interest (ROI) applies threshold to the paricular co-ordinates passed

    '''
    Important Note:
    The tesseract is an efficient engine while converting image to string as it is trained over many languages
    But it performed poorly, when subjected to reading characters from number plate especially HSRP number plate which are widely used in India
    So, a font called "License Plate" available from the internet, created in the year 2005 and has a close resemblance to the HSRP characters
    I have extracted this font, and trained tesseract on this font, to recognize the HSRP characters with high accuracy
    For training, I have used 500 pages with 10000 iterations which took about 8 hours to complete in Google Colab
    The font achieved from the training is what used in this project to detect HSRP characters
    Although the model performs better than plain english, but still it has to go a long way to be efficient and accurate
    Camera angles, lighting, type of camera, resolution, all these things matter.
    That's the reason, lang='LicensePlate' is used in the below line
    This file will be made available in the repository under the name - "LicensePlate.traineddata"
    Please add the file to this directory : /usr/share/tesseract-ocr/4.00/tessdata
    Or use lang='eng' to avoid runtime error
    '''
    data = pytesseract.image_to_string(ROI, lang='LicensePlate',
                                       config='--psm 6 /usr/share/tesseract-ocr/4.00/tessdata/configs/custom.txt').upper()
    # here, we used custom.text as the config file which was declared earlier

    # print(data)     # It displays data in multiline format, for eg., it prints 2 lines if license plate has 2 lines
    list_of_data = list(data)  # We convert that to list
    # print(list_of_data)
    # "\n" represents new line and "\x0c" represents tab space
    modified_data = ""  # We convert that multiline data into single line by replacing characteres such as "\n" and "\x0c"
    for char in list_of_data:
        if char == "\n" or char == "\x0c":
            continue
        modified_data += char
    # print(modified_data)        # We print the modified data in a single line
    # print(len(data))
    # cv2.imshow('thresh', thresh)  #entire image with threshold applied
    # cv2.imshow('ROI', ROI)  #number_plate with threshold applied and cropped
    cv2.waitKey(0)
    return modified_data  # we return the modified data ready to be called from different modules


# helpful while running the program as standalone
if __name__ == '__main__':
    get_date_and_time(img_name)
    get_license_plate_info(img_name)
    # get_license_plate_info(img_name, 207, 217, 455, 97)


# a simple fetch_date and time() is created, so that, when we call the get_date_and_time from other modules, we don't have to pass the required arguments everytime
def fetch_date_and_time():
    accessable_date = date  # local variable accessable_date stores the global date value
    accessable_time = time  # local variable accessable_time stores the global time value
    return accessable_date, accessable_time  # return the values, when called from other modules
