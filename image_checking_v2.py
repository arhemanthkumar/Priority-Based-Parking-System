import cv2

image_path = '/home/hemanth/PycharmProjects/Priority-Based-Parking-System/images/TC_00015.jpg'
image = cv2.imread(image_path, 1)

if image is None:
    print(f"Error: Unable to load image from {image_path}")
else:
    print("Image loaded successfully")
    cv2.imshow("Loaded Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
