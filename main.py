import os  # imports os module to get current directory information and allows us to change directory on demand
import cv2  # imports cv2 module for image manipulation and image processing
import numpy as np  # Imports numpy module for numerical operations on arrays and matrices
import time  # imports time module to introduce delay in the program
import ODS  # importing ODS.py file
import argparse  # imports argparse module for command-line argument parsing
import pandas as pd  # imports pandas library to handle vehicle data
import Character_Recognition  # imports Character_Recognition .py file

vehicle_type = ""  # stores vehicle class that is 2-wheeler or 4-wheeler
lic_no = ""  # stores license plate number


# Around 90% of the code is from the source of YOLOv4, which can be modified directly from https://github.com/AlexeyAB/darknet/blob/master/darknet.py
# Yolov4 calculates bounding boxes, makes predictions and displays interference
class Yolov4:

    def __init__(self, weights, cfg, img_size=320):
        self.weights = weights  # path to weights file named as "yolov4.weights"
        self.cfg = cfg  # path to configuration file names as "yolov4.cfg"
        self.classes = ['license_plate', '2_wheeler', '4_wheeler']  # list of class labels for object detection
        self.Neural_Network = cv2.dnn.readNetFromDarknet(self.cfg,
                                                         self.weights)  # loads the YOLO model with the given configuration and weights
        self.outputs = self.Neural_Network.getUnconnectedOutLayersNames()  # gets the names of the output layers
        self.COLORS = np.random.randint(0, 255, size=(len(self.classes), 3),
                                        dtype="uint8")  # generates random colors for each class
        self.image_size = img_size  # size to which the input image will be resized for the model

    def bounding_box(self, detections):  # bounding_box() calculates bounding boxes
        try:
            confidence_score = []  # list to store confidence score of the objects detected
            ids = []  # list to store class IDs
            cordinates = []  # stores bounding box coordinates in the form of list
            Threshold = 0.6  # confidence threshold for detections for object identification
            for i in detections:  # iterate through detections
                for j in i:  # iterate through each detection
                    probs_values = j[5:]  # class probabilities
                    class_ = np.argmax(probs_values)  # identify class with the highest probability
                    confidence_ = probs_values[class_]  # get confidence of the identified class

                    if confidence_ > Threshold:  # check if confidence is above threshold
                        w, h = int(j[2] * self.image_size), int(j[3] * self.image_size)  # calculate width and height
                        x, y = int(j[0] * self.image_size - w / 2), int(
                            j[1] * self.image_size - h / 2)  # calculate top-left corner coordinates
                        cordinates.append([x, y, w, h])  # add coordinates to list
                        ids.append(class_)  # add class ID to list
                        confidence_score.append(float(confidence_))  # add confidence score to list

            # apply non-maximum suppression to eliminate redundant overlapping boxes
            final_box = cv2.dnn.NMSBoxes(cordinates, confidence_score, Threshold, .6)

            # return final boxes, coordinates, confidence scores, and class IDs
            return final_box, cordinates, confidence_score, ids

        except Exception as e:
            print(f'Error in : {e}')  # print error message

    def predictions(self, prediction_box, bounding_box, confidence, class_labels, width_ratio, height_ratio, end_time,
                    image):
        global vehicle_type  # reference to global variable vehicle_type so that it can be accessed from outside the function and from other modules
        global lic_no  # reference to global variable lic_no so that it can be accessed from outside the function and from other modules
        try:
            temp = []  # temporary list to keep track of labels
            boundary_of_license_plate = []  # list to store license plate boundaries
            for j in prediction_box.flatten():  # iterate through prediction boxes
                x, y, w, h = bounding_box[j]  # get bounding box coordinates
                x = int(x * width_ratio)  # adjust x-coordinate based on original image size
                y = int(y * height_ratio)  # adjust y-coordinate based on original image size
                w = int(w * width_ratio)  # adjust width based on original image size
                h = int(h * height_ratio)  # adjust height based on original image size
                label = str(self.classes[class_labels[j]])  # get class label
                if label not in temp:  # check if label is not already processed
                    temp.append(label)  # add label to temporary list
                    conf_ = str(round(confidence[j], 2))  # round and convert confidence to string
                    color = [int(c) for c in self.COLORS[class_labels[j]]]  # get color for the class
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)  # draw rectangle around detected object
                    cv2.putText(image, label + ' ' + conf_, (x, y - 2), cv2.FONT_HERSHEY_COMPLEX, .8, color,1)  # put class label and confidence on the image

                    # time_str = f"Inference time: {end_time:.3f} sec"
                    # cv2.putText(image, time_str, (10, 30), cv2.FONT_HERSHEY_COMPLEX, .5, (156, 0, 166), 1)
                    # print(j, label, conf_, x, y, w, h)

                    if label != 'license_plate':  # if detected object is not a license plate
                        # print("Vehicle Type: ",label)
                        vehicle_type = label  # update vehicle_type
                    if label == 'license_plate':  # if detected object is a license plate
                        license_number = Character_Recognition.get_license_plate_info(image_filename, x, y, w, h)  # extract license number using Character_Recognition module
                        Character_Recognition.get_date_and_time(
                            image_filename)  # extract date and time from the image using Character_Recognition module
                        lic_no = license_number  # update lic_no
            return image  # return annotated image

        except Exception as e:
            print(f'Error in : {e}')  # print error message

    def Inference(self, image, original_width, original_height):
        try:
            # Resize image to network input size
            resized_image = cv2.resize(image, (
            self.image_size, self.image_size))  # resize image to the input size expected by the model
            blob = cv2.dnn.blobFromImage(resized_image, 1 / 255, (self.image_size, self.image_size), True,
                                         crop=False)  # convert image to blob and set it as input to the neural network
            self.Neural_Network.setInput(blob)
            start_time = time.time()  # record start time
            output_data = self.Neural_Network.forward(self.outputs)  # run forward pass to get detections
            end_time = time.time() - start_time  # calculate inference time
            final_box, cordinates, confidence_score, ids = self.bounding_box(
                output_data)  # filter and extract bounding boxes
            outcome = self.predictions(final_box, cordinates, confidence_score, ids,
                                       original_width / self.image_size,
                                       original_height / self.image_size, end_time,
                                       image)  # annotate image and extract information
            return outcome  # return annotated image
        except Exception as e:
            print(f'Error in : {e}')  # print error message

    def getLicenseAndClass(self):
        get_lic_no = lic_no  # get license number
        get_vehicle_class = vehicle_type  # get vehicle type
        return get_lic_no, get_vehicle_class  # return license number and vehicle type


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='yolov4.weights', help='weights path')  # add argument for weights path
    parser.add_argument('--cfg', type=str, default='yolov4.cfg', help='cfg path')  # add argument for configuration file path
    parser.add_argument('--image', type=str, default='', help='image path')  # add argument for image path
    parser.add_argument('--video', type=str, default='', help='video path')  # add argument for video path
    parser.add_argument('--img_size', type=int, default=320, help='size of w*h')  # add argument for image size
    opt = parser.parse_args()  # Parse arguments

    obj = Yolov4(weights=opt.weights, cfg=opt.cfg, img_size=opt.img_size)  # create Yolov4 object with parsed arguments

    if opt.image:  # if image path is provided
        try:
            # print(os.getcwd()) # our working directory
            os.chdir("input_images")  # change directory to input_images

            image_path = opt.image  # get image path
            image_filename = os.path.basename(opt.image)  # get image filename

            if not os.path.isfile(
                    image_path):  # if the image is not found in the directory, raises the FileNotFoundError exception
                raise FileNotFoundError(f"Error: File {image_path} does not exist or cannot be read.")
            image = cv2.imread(opt.image, 1)  # read image
            original_width, original_height = image.shape[1], image.shape[0]  # get original width and height of the image
            outcome = obj.Inference(image=image, original_width=original_width, original_height=original_height)  # run inference
            # cv2.imshow('Inference', outcome)
            cv2.waitKey(0)  # essential to wait for key press when the image is shown
            cv2.destroyAllWindows()
            os.chdir("..")  # going back to the parent directory

            # print(os.getcwd())
            # testing_python_simple.dateplease()

            ODS.ods(vehicle_type, lic_no)  # save vehicle type and license number using ODS module
        except Exception as e:
            print(f'Error in : {e}')  # print error message
