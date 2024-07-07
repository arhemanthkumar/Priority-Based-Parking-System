
# Vehicle Movement Analysis and Insight Generation in a College Campus using Edge AI

## Overview
This project is mainly developed for Vehicle Movement Analysis and Insight Generation for all the vehicles entering the parking space of the college campus using Edge AI.\
Efforts have been made to develop this project using Open Source Software where ever possible.\
It provides an innovative solution designed to streamline and automate vehicle management in parking lots.\
Leveraging advanced machine learning and computer vision technologies, this system provides real-time tracking and management of vehicles, optimizing parking space utilization and enhancing user convenience.

## Key Features
### 1. Vehicle Detection and Recognition:
- **Object Detection**: Utilizes a YOLO-based (You Only Look Once) deep learning model to detect vehicles entering and exiting the parking lot. It successfully identifies the vehicles as 2-wheeler or 4-wheeler.
- **License Plate Recognition**: Employs Tesseract OCR, trained on custom fonts, to accurately read and recognize license plates.

### 2. Data Management:
- **Real-Time Tracking**: Monitors vehicle entry and exit, updating the status in real time.
- **Parking Space Availability**: Keeps track of occupied and available parking spaces, dynamically updating as vehicles enter or exit.
- **Historical Data Storage**: Stores vehicle data, including date, time, vehicle class, license plate number, registration status, and parking status in an ODS (OpenDocument Spreadsheet) file.

### 3. Web Interface:
- **Visualization**: Provides a user-friendly web interface to display real-time data and historical trends.
- **Graphical Representation**: Features line graphs showing occupied and available parking spaces over time, facilitating quick and easy monitoring.

### 4. Automation:
- **Batch Processing**: Capable of processing multiple images with different parameters in a batch, ensuring efficient and continuous data updates.

## Technical Implementation
- **Image Processing**: The system processes images and videos captured from surveillance cameras, detecting vehicles and recognizing license plates using the YOLO model and Tesseract OCR.
- **Data Storage**: Utilizes ODS files to store vehicle data, ensuring easy access and management.
- **Web Development**: The web interface is built using Flask, a lightweight Python web framework, and incorporates Plotly for dynamic data visualization.
- **Training**: The Tesseract OCR model is trained on 500 pages of text with 10000 iterations to achieve high accuracy in recognizing custom fonts used on license plates.

## Benefits
- **Efficiency**: Automates the process of vehicle tracking and parking space management, reducing manual effort and errors.
- **Real-Time Monitoring**: Provides up-to-the-minute data on parking space availability, improving the user experience.
- **Data-Driven Decisions**: Offers detailed insights into parking usage patterns, aiding in better decision-making and resource allocation.
- **Scalability**: Designed to handle large volumes of data, making it suitable for deployment in large parking facilities.

## Future Enhancements
- **Mobile Application**: Develop a mobile app for users to check parking availability in real-time.
- **Integration with Payment Systems**: Incorporate automated payment processing for seamless entry and exit.
- **Advanced Analytics**: Implement predictive analytics to forecast parking space availability based on historical data.

## Authors

- [@arhemanthkumarar](https://www.github.com/arhemanthkumarar)


## Badges


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](https://opensource.org/licenses/)

[![GMAIL](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://github.com/torvalds/linux)

[![](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

[![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[![](https://img.shields.io/badge/YOLOv4-blue?style=flat&color=%2330B3FE
)](https://github.com/AlexeyAB/darknet)

[![](https://img.shields.io/badge/Tesseract%20-orange
)](https://github.com/tesseract-ocr/tesseract)

[![](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)](https://html.spec.whatwg.org/)

[![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/en/3.0.x/)


## Demo (Must Watch [Mandatory] )

https://www.youtube.com/watch?v=ufMk-Uj_W8c


## Install and Run Locally (For Linux)

#### For linux, use "python3" in the commands
#### For Windows, use "python" in the commands
\
Clone the project

```bash
  git clone https://github.com/arhemanthkumar/Priority-Based-Parking-System.git
```
\
Go to the project directory

```bash
  cd Priority-Based-Parking-System
```
\
Install dependencies

```bash
  pip install -r requirements.txt
```

\
Copy custom LicensePlate Font trained data to the directory where Tesseract languages are stored

```bash
  sudo cp LicensePlate.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```
Confirm the Tesseract version before proceeding


\
Also, add the config file custom.txt to tesseract config file which whitelist only allowable characters from the license plate such as "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
``` bash
  sudo cp custom.txt /usr/share/tesseract-ocr/4.00/tessdata/configs/
```
Confirm the Tesseract version before proceeding


\
You can check Vehicle.ods file, right now, it contains the list of Vehicles entered and exited the campus along with few other parameters. Double click and see the contents

\
Be sure to delete the Vehicle.ods file or move it to a different directory, as it overwrites the contents again when the program is runned

```bash
  rm Vehicle.ods
```
This will remove the Vehicle.ods file from the directory

Don't worry, it will be automatically created again when the program starts with the fresh data

\
If you have to run on a single instance of a single image, then run

```bash
  python3 main.py --image=/home/hemanth/PycharmProjects/Priority-Based-Parking-System/input_images/imgxxx.jpg --img_size=320
```
where xxx is the image name which starts from 0, 1, 2, ..., 208 which are located inside "input_images" folder.

For example, img0, img1, img2, img3, ...., upto img208

\
If you wish to run the script, which saves the manual work and goes through all the images automatically at a time, then run

```bash
  python3 batch.py
```
This will process all the images inside the "input_images" folder with a delay of 3 second for each iteration

In both the cases, you can observe the data being entered into the Vehicle.ods file which is newly created automatically

This will take some time, so sit back and relax

\
To view the analysis, in a interactive webpage

Meanwhile, you can open another terminal instance in the same directory or enter the command after running for single image

```bash
  python3 app.py
```

Right click on the link -> Open Link

The link looks like this: http://127.0.0.1:5000

This containes the Flask app which is integrated with the index.html file inside templates folder

Here, you can see, Parking Occupany Graph with Live Count of Vehicles and many more parameters



## Note

The input images used in the project are taken by me (author - [@arhemanthkumarar](https://www.github.com/arhemanthkumarar)) inside
the college campus with prior notice
to the management and with the
consent of the respective vehicle
owners.


Although only entry time of the
vehicles could be captured, for
better simulating vehicle movement
and for the purpose to keep a track
of vehicle occupancy in the parking
space, exit times of the vehicles
are modified according to the needs.


## Screenshots

![Glimpse](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/9d036a23-a4ec-4565-aad1-c47b3fe33ef2)
\
![Terminal](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/48e6b5b1-3afa-451f-b8e7-b6138115a9f7)
\
![Graph](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/b27731de-3b69-4cb2-b711-14047524993f)



## Optimizations

#### Red lines -> mAP% - Mean Average Precision percentage (It denotes accuracy) [Higher is better]
#### Blue lines -> Loss (It denotes error rate) [Lower is better]

Initially, while trying Yolov4 with 5 classes with training time of around ~ 18 hours


![initial_yolo](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/69e7bc56-a028-4e20-9247-3d9eaa14b1e7)

The performance of the system was not satisfactory.

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/4808c892-88d6-4fdb-9eeb-8a05cbbcf929)

We can also observe multiple false detections and cropping of time and date

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/ac16d09b-c36d-4bf3-b3a4-8c1dab385969)

\
To tackle the issue, the date and time are directly extracted from the image instead of detecting as the object.\
This reduced training train from 18 to 10 hours and much better accuracy.

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/dfab688d-be0e-4110-8fc4-7404b8a2ad47)

The results observed were much more satisfying

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/be406eea-aa49-49fd-b3f8-7f99bc0140aa)

There were no overlapping of bounding boxes plus high confidence levels observed

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/60470a39-9d86-410e-9d8f-e0271c7594a3)

These training weights were extracted and saved under the name "yolov4.weights"

To annotate the images, I have used https://www.makesense.ai/ which helped me create annotations to images which were used for training Yolov4

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/0c29eca8-8a56-4e5a-ae7e-7ec43419b8c8)

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/e34ea145-28c7-45c5-bf03-e4fe8bb4b38c)

\
Also the font used in Indian HSRP was not detected easily with Tesseract, although it is a capable engine.\
So, I had to train tesseract to detect custom font obtained from internet with close resemblence with 500 pages and max-iteration of 10000

![image](https://github.com/arhemanthkumar/Priority-Based-Parking-System/assets/99478864/7b64f2cd-9641-4b58-adf1-ed9370ee9d81)

This surely increased, character recognition capability to some certain extent, but still improvements are needed
