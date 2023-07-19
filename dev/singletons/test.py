import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.stats import linregress

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))

    for idx, kp in enumerate(shaped):
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)
            cv2.putText(frame, str(idx), (int(kx), int(ky)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

def calculate_slope_and_annotate(image_np, midpoints_x, midpoints_y, person_idx):
    # Calculate the slope of the line using a linear regression
    if len(midpoints_x) >= 2 and len(midpoints_y)  >= 2: 
        slope, intercept, r_value, p_value, std_err = linregress(midpoints_x, midpoints_y)
        
        # Draw text on image
        text = f"Slope: {slope:.2f}"
        position = (30, 30 + person_idx * 50)
        ax.text(position[0], position[1], text, color='red', fontsize=12, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

def loop_through_people(frame, keypoints_and_scores, edges, confidence_threshold):
    for person in keypoints_and_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)

# Load the pose estimation model from TensorFlow Hub
model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']

# Load the image
image = Image.open('image1.jpg').convert('RGB')

# Convert the image to numpy array
image_np = np.array(image)

# Resize the image to the size the model expects and add a batch dimension
image = tf.image.resize(image_np, (384, 640))
image = tf.expand_dims(image, axis=0)

# Run the image through the model
outputs = movenet(tf.cast(image, dtype=tf.int32))

# The output is a dictionary with a 'output_0' key that contains the pose keypoints
keypoints_with_scores = outputs['output_0'].numpy()[:,:,:51].reshape((6,17,3))

loop_through_people()