import os
import cv2
import numpy as np
from utils import get_face_landmarks
# import concurrent.futures
# data directory
# data_dir = './Newdata'
data_dir = './AugmentedData'

print("Current Working Directory:", os.getcwd())
print(os.path.abspath(data_dir))

# Limit the number of threads to avoid excessive thread creation
os.environ["OMP_NUM_THREADS"] = "4"

# Function to process each image and extract face landmarks
def process_image(image_path, emotion_indx):
    print("Processing", image_path)
    image = cv2.imread(image_path)
    face_landmarks = get_face_landmarks(image)
    
    # Check if the face_landmarks length is valid (1404 as in the original code)
    if len(face_landmarks) == 1404:
        face_landmarks.append(int(emotion_indx))
        return face_landmarks
    return None

# Get list of all images to process
all_images = []
for emotion_indx, emotion in enumerate(sorted(os.listdir(data_dir))):
    emotion_dir = os.path.join(data_dir, emotion)
    for image_file in os.listdir(emotion_dir):
        image_path = os.path.join(emotion_dir, image_file)
        all_images.append((image_path, emotion_indx))


# Function to process a batch of images and save to a text file
def process_batch(batch, output_file):
    output = []
    for x in batch:
        result = process_image(x[0], x[1])
        if result:
            output.append(result)
    
    # Save the batch to a text file
    np.savetxt(output_file, np.asarray(output))

# Process each batch and save to separate files
process_batch(all_images, 'data6_part.txt') #1

print("Data saved")

