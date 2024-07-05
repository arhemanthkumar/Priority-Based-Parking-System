import cv2
import numpy as np
from pytesseract import pytesseract
from craft_text_detector import Craft

def padd_image(image):
    # set padding size
    padding_size = 50

    # padd with black pixels
    padded_image = np.zeros((image.shape[0] + 2 * padding_size, image.shape[1] + 2 * padding_size, 3), dtype=np.uint8)
    padded_image[padding_size:padding_size + image.shape[0], padding_size:padding_size + image.shape[1]] = image

    return padded_image


def get_rois(image):
    # get ROIs for text using CRAFT
    text_rois = Craft.detect_text(image)['boxes']

    # get rois
    rois = []
    for roi in text_rois:
        if len(roi) >= 3:  # ensure at least 3 points for a polygon

            # convert box points to numpy array for easier manipulation
            box_points = np.array(roi, dtype=np.int32).reshape(-1, 2)

            # calculate the minimum bounding rectangle
            rotated_rect = cv2.minAreaRect(box_points)

            # get vertices of box
            box_vertices = cv2.boxPoints(rotated_rect)
            box_vertices = np.int0(box_vertices)

            # append box_vertices on angled_rois list
            rois.append(box_vertices)

    return rois


def rotate_text_image(image, angled_rois):
    # get largest roi
    largest_roi = max(angled_rois, key=cv2.contourArea)

    # get fitted line
    [vx, vy, x, y] = cv2.fitLine(largest_roi, cv2.DIST_L2, 0, 0.01, 0.01)

    # get angle
    angle_rad = np.arctan2(vy, vx)
    angle = np.degrees(angle_rad)[0]

    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    # if angle made by roi is 90 degree then no rotation needed
    if angle != 90:
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
        image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return image


def extract_text(image, text_rois):
    # copy of image
    img_text = image.copy()

    for index, roi in enumerate(text_rois):
        # get the bounding box from the angled ROI
        x, y, w, h = cv2.boundingRect(roi)

        # get text using pytesseract
        text_roi = image[y: y + h, x: x + w]

        # little Preprocessing
        roi_gray = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)

        # get lines of text from pytesseract
        text_line = f'Line {index + 1} : ' + pytesseract.image_to_string(roi_gray, lang='LicensePlate', config='/usr/share/tesseract-ocr/4.00/tessdata/configs/custom.txt')

        # Put text on image
        cv2.putText(img_text, text_line.strip('\n'), (0, 30 + (index) * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                    2, cv2.LINE_AA)

    return img_text


def extract_text_from_deskewed_text_image(image):
    # padd image
    img = padd_image(image)

    # get angled rois
    angled_rois = get_rois(img)

    # rotate text_image
    if angled_rois:
        img = rotate_text_image(img, angled_rois)

    # get deskewed rois
    deskewed_rois = get_rois(img)

    # extract text
    img_text = extract_text(img, deskewed_rois)

    return img_text

extract_text_from_deskewed_text_image("TC_00009.jpg")