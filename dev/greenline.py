import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.stats import linregress


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

# Load the pose estimation model from TensorFlow Hub
model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']

# Load the image
image = Image.open('image10.jpg').convert('RGB')

# Convert the image to numpy array
image_np = np.array(image)

# Resize the image to the size the model expects and add a batch dimension
image = tf.image.resize(image_np, (384, 640))
image = tf.expand_dims(image, axis=0)

# Run the image through the model
outputs = movenet(tf.cast(image, dtype=tf.int32))

# The output is a dictionary with a 'output_0' key that contains the pose keypoints
keypoints_with_scores = outputs['output_0'].numpy()[:,:,:51].reshape((6,17,3))

print(keypoints_with_scores)

pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]

# Create a figure and axes
fig, ax = plt.subplots()

# Display the image on the axes
ax.imshow(image_np)

keypoint_confidence_threshold = 0.5  # You can adjust this value as needed
min_keypoints = 5 

for person_idx, person in enumerate(keypoints_with_scores):
    # Select only the confidence scores of keypoints that are above a certain threshold
    high_confidence_scores = person[person[:,2] > 0.2, 2]

    # Calculate the average confidence score of the high-confidence keypoints
    avg_high_confidence_score = high_confidence_scores.mean() if high_confidence_scores.size > 0 else 0

    print(f"Iterating on personIDX: {person_idx} with average high-confidence keypoint score of {avg_high_confidence_score}")

    # Skip this person if the average high-confidence keypoint score is below the threshold
    if avg_high_confidence_score < keypoint_confidence_threshold:
        print(f"Skipping person {person_idx} because average of high-confidence keypoint scores {avg_high_confidence_score} <  {keypoint_confidence_threshold}")
        continue
    #print(f"Person IDX: {person_idx} Scores: {scores}")

for person_idx, person in enumerate(keypoints_with_scores):
    # # Select only the confidence scores of keypoints that are above a certain threshold
    # high_confidence_scores = person[person[:,2] > 0.1, 2]

    # # Calculate the average confidence score of the high-confidence keypoints
    # avg_high_confidence_score = high_confidence_scores.mean() if high_confidence_scores.size > 0 else 0

    # print(f"Iterating on personIDX: {person_idx} with average high-confidence keypoint score of {avg_high_confidence_score}")

    # # Skip this person if the average high-confidence keypoint score is below the threshold
    # if avg_high_confidence_score < keypoint_confidence_threshold:
    #     print(f"Skipping person {person_idx} because average of high-confidence keypoint scores {avg_high_confidence_score} <  {keypoint_confidence_threshold}")
    #     continue

    midpoints_x = []
    midpoints_y = []

    # For each pair of keypoints, calculate the midpoint and add it to the lists
    for i, j in pairs:
        if person[i][2] > 0.1 and person[j][2] > 0.1:
            midpoint_x = (person[i][1] + person[j][1]) / 2
            midpoint_y = (person[i][0] + person[j][0]) / 2
            midpoints_x.append(midpoint_x)
            midpoints_y.append(midpoint_y)

    # Convert coordinates to image's scale
    midpoints_x_img = np.array(midpoints_x) * image_np.shape[1]
    midpoints_y_img = np.array(midpoints_y) * image_np.shape[0]

    # Calculate slope and annotate image
    if midpoints_x_img.size != 0 and midpoints_y_img.size != 0: 
        calculate_slope_and_annotate(image_np, midpoints_x_img, midpoints_y_img, person_idx)
    
    
    # Plot a line connecting the midpoints
    ax.plot(midpoints_x_img, midpoints_y_img, 'g-')



    # Plot a line connecting the midpoints
    # plt.plot(np.array(midpoints_x) * image_np.shape[1], np.array(midpoints_y) * image_np.shape[0], 'g-')

for person in keypoints_with_scores:
    for y, x, c in person:
        if c > 0.1:  # 0.1 is the confidence threshold
            plt.plot(x * image_np.shape[1], y * image_np.shape[0], 'ro')

ax.axis('off')  # to remove axes

plt.show()

# # Display the image
# plt.imshow(image_np)

# To save the image
fig.savefig('output_with_midline.jpg', bbox_inches='tight', pad_inches=0)

