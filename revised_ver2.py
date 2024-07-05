import os
import cv2
import numpy as np
import time
import ODS
import argparse
import pandas as pd
import test2

vehicle_type = ""
lic_no = ""


class Yolov4:

    def __init__(self, weights, cfg, img_size=320):
        self.weights = weights
        self.cfg = cfg
        self.classes = ['license_plate', '2_wheeler', '4_wheeler']
        self.Neural_Network = cv2.dnn.readNetFromDarknet(self.cfg, self.weights)
        self.outputs = self.Neural_Network.getUnconnectedOutLayersNames()
        self.COLORS = np.random.randint(0, 255, size=(len(self.classes), 3), dtype="uint8")
        self.image_size = img_size

    def bounding_box(self, detections):
        try:
            confidence_score = []
            ids = []
            cordinates = []
            Threshold = 0.6
            for i in detections:
                for j in i:
                    probs_values = j[5:]
                    class_ = np.argmax(probs_values)
                    confidence_ = probs_values[class_]

                    if confidence_ > Threshold:
                        w, h = int(j[2] * self.image_size), int(j[3] * self.image_size)
                        x, y = int(j[0] * self.image_size - w / 2), int(j[1] * self.image_size - h / 2)
                        cordinates.append([x, y, w, h])
                        ids.append(class_)
                        confidence_score.append(float(confidence_))

            final_box = cv2.dnn.NMSBoxes(cordinates, confidence_score, Threshold, .6)

            return final_box, cordinates, confidence_score, ids

        except Exception as e:
            print(f'Error in : {e}')

    def predictions(self, prediction_box, bounding_box, confidence, class_labels, width_ratio, height_ratio, end_time,
                    image):
        global vehicle_type
        global lic_no
        try:
            temp = []
            boundary_of_license_plate = []
            for j in prediction_box.flatten():
                x, y, w, h = bounding_box[j]
                x = int(x * width_ratio)
                y = int(y * height_ratio)
                w = int(w * width_ratio)
                h = int(h * height_ratio)
                label = str(self.classes[class_labels[j]])
                if label not in temp:
                    temp.append(label)
                    conf_ = str(round(confidence[j], 2))
                    color = [int(c) for c in self.COLORS[class_labels[j]]]
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(image, label + ' ' + conf_, (x, y - 2), cv2.FONT_HERSHEY_COMPLEX, .8, color, 1)
                    # time_str = f"Inference time: {end_time:.3f} sec"
                    # cv2.putText(image, time_str, (10, 30), cv2.FONT_HERSHEY_COMPLEX, .5, (156, 0, 166), 1)

                    # print(j, label, conf_, x, y, w, h)
                    if label != 'license_plate':
                        print("Vehicle Type: ",label)
                        vehicle_type = label
                    if label == 'license_plate':
                        license_number = test2.get_license_plate_info(image_filename, x, y, w, h)
                        test2.get_date_and_time(image_filename)
                        lic_no = license_number
            return image

        except Exception as e:
            print(f'Error in : {e}')

    def Inference(self, image, original_width, original_height):
        try:
            # Resize image to network input size
            resized_image = cv2.resize(image, (self.image_size, self.image_size))
            blob = cv2.dnn.blobFromImage(resized_image, 1 / 255, (self.image_size, self.image_size), True, crop=False)
            self.Neural_Network.setInput(blob)
            start_time = time.time()
            output_data = self.Neural_Network.forward(self.outputs)
            end_time = time.time() - start_time
            final_box, cordinates, confidence_score, ids = self.bounding_box(output_data)
            outcome = self.predictions(final_box, cordinates, confidence_score, ids,
                                       original_width / self.image_size,
                                       original_height / self.image_size, end_time, image)
            return outcome
        except Exception as e:
            print(f'Error in : {e}')

    def getLicenseAndClass(self):
        get_lic_no = lic_no
        get_vehicle_class = vehicle_type
        print("From here", get_vehicle_class)
        return get_lic_no, get_vehicle_class

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='yolov4.weights', help='weights path')
    parser.add_argument('--cfg', type=str, default='yolov4.cfg', help='cfg path')
    parser.add_argument('--image', type=str, default='', help='image path')
    parser.add_argument('--video', type=str, default='', help='video path')
    parser.add_argument('--img_size', type=int, default=320, help='size of w*h')
    opt = parser.parse_args()

    obj = Yolov4(weights=opt.weights, cfg=opt.cfg, img_size=opt.img_size)

    if opt.image:
        try:
            # print(os.getcwd()) #Our working directory
            os.chdir("images") #Directory of the images

            image_path = opt.image
            image_filename = os.path.basename(opt.image)

            if not os.path.isfile(image_path): #If the image is not found in the directory, raises the FileNotFoundError exception
                raise FileNotFoundError(f"Error: File {image_path} does not exist or cannot be read.")
            image = cv2.imread(opt.image, 1)
            original_width, original_height = image.shape[1], image.shape[0]
            outcome = obj.Inference(image=image, original_width=original_width, original_height=original_height)
            cv2.imshow('Inference', outcome)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            os.chdir("..") #Going back to the parent directory
            # print(os.getcwd())
            # testing_python_simple.dateplease()
            print("IMP1",vehicle_type)
            print("IMP2",lic_no)




            ODS.ods(vehicle_type, lic_no)
        except Exception as e:
            print(f'Error in : {e}')

    if opt.video:
        try:
            cap = cv2.VideoCapture(opt.video)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output = cv2.VideoWriter("demo.avi", fourcc, fps, (width, height))

            while cap.isOpened():
                res, frame = cap.read()
                if res:
                    outcome = obj.Inference(image=frame, original_width=width, original_height=height)
                    cv2.imshow("demo", outcome)
                    output.write(outcome)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break

            cap.release()
            output.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f'Error in : {e}')

