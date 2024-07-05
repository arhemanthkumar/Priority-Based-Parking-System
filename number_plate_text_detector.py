from PIL import Image
from pytesseract import pytesseract
import os
# os.system('cd "/home/hemanth/Desktop/yolov4_old"')
os.chdir('/home/hemanth/Desktop/yolov4_old/darknet')
# print(os.curdir)
print(os.getcwd())
os.system('./darknet detector test data/obj.data cfg/yolov4-custom.cfg ../training/yolov4-custom_best.weights /home/hemanth/Desktop/number_plate_images/TC_00099.JPG -thresh 0.6')