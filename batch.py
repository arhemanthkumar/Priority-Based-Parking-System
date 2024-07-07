import os
import time


# Function to process each image
def process_image(image_path):
    # Add your image processing logic here
    print(f"Processing image: {image_path}")
    # Replace with your processing logic for each image
    # Example: run command
    command = f"python3 main.py --image={image_path} --img_size=320"
    os.system(command)


# Directory where images are located
image_dir = "/home/hemanth/PycharmProjects/Priority-Based-Parking-System/input_images"

# List all image files in the directory
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(".jpg")],
                     key=lambda x: int(x.split("img")[1].split(".")[0]))

# Process each image sequentially
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    process_image(image_path)

    # Add delay between processing each image
    time.sleep(3)  # 5 second delay between each image processing
