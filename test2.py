# To detect time-stamps from the bottom left of the image.
from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract

img = Image.open("IMG_2752.JPG")
# img.show()

box = (0, 2850, 1370, 3050)
img2 = img.crop(box)

croppedImage = "cropped_image.png"
img2.save(croppedImage)
# img2.show()

img3 = Image.open(croppedImage)

text = pytesseract.image_to_string(img3)
print(text)
