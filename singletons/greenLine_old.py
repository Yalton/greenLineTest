import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.stats import linregress
import matplotlib.patches as patches

# Set the debug variable
debug = True

def calculate_slope_and_annotate(ax, midpoints_x, midpoints_y, person_idx, image_width, image_height):
    if len(midpoints_x) >= 2 and len(midpoints_y) >= 2:
        slope, intercept, r_value, p_value, std_err = linregress(midpoints_x, midpoints_y)
        verticality_percentage = abs(slope) / (1 + abs(slope)) * 100
        text = f"Person #{person_idx + 1} Chad Score: {verticality_percentage:.2f}%"

        # Scale the position and font size based on image width and height
        position = (image_width * 0.05, image_height * (0.005 + person_idx * 0.05))
        fontsize = np.log(width) * 2

        ax.text(position[0], position[1], text, color='green', fontsize=fontsize, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))


def get_bounding_box(keypoints):
    min_x = np.min(keypoints[:, 1])
    min_y = np.min(keypoints[:, 0])
    max_x = np.max(keypoints[:, 1])
    max_y = np.max(keypoints[:, 0])
    return [min_y, min_x, max_y, max_x]

def check_overlap(box1, box2):
    return not (box1[2] < box2[0] or box1[0] > box2[2] or box1[3] < box2[1] or box1[1] > box2[3])

# Load the SSD MobileNet model from TensorFlow Hub
ssd_mobilenet = hub.load('https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2')

# Load the pose estimation model from TensorFlow Hub
movenet = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1').signatures['serving_default']

# Load the image
image = Image.open('image10.jpg').convert('RGB')

# Convert the image to numpy array
image_np = np.array(image)

# Convert the image to the size the SSD MobileNet model expects and add a batch dimension
input_tensor = tf.convert_to_tensor(image_np)
input_tensor = input_tensor[tf.newaxis,...]

# Run the image through the SSD MobileNet model
output_dict = ssd_mobilenet(input_tensor)

# The output is a dictionary with keys for 'detection_scores', 'detection_classes', and 'detection_boxes'
scores = output_dict['detection_scores'].numpy()[0]
classes = output_dict['detection_classes'].numpy()[0]
boxes = output_dict['detection_boxes'].numpy()[0]

# Resize the image to the size the model expects and add a batch dimension
image = tf.image.resize(image_np, (384, 640))
image = tf.expand_dims(image, axis=0)

# Run the image through the model
outputs = movenet(tf.cast(image, dtype=tf.int32))

# The output is a dictionary with a 'output_0' key that contains the pose keypoints
keypoints_with_scores = outputs['output_0'].numpy()[:,:,:51].reshape((6,17,3))

#pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (5, 6), (11, 12), (13, 14), (15, 16)]
pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]

# Create a figure and axes
fig1, ax1 = plt.subplots(figsize=(10, 10))  # For bounding boxes
fig2, ax2 = plt.subplots(figsize=(10, 10))  # For midlines and slope annotations

# Display the image on the axes
#ax1.imshow(image_np)
ax2.imshow(image_np)

# Define a threshold for the detection score
score_threshold = 0.5

boxes_img_scale = boxes * [image_np.shape[0], image_np.shape[1], image_np.shape[0], image_np.shape[1]]

# Filter the bounding boxes based on the detection class and score
people_boxes = boxes_img_scale[(classes == 1) & (scores > score_threshold)]

# Iterate through each bounding box
for box_idx, box in enumerate(people_boxes):
    ymin, xmin, ymax, xmax = box
    ymin, ymax = ymin * image_np.shape[0], ymax * image_np.shape[0]
    xmin, xmax = xmin * image_np.shape[1], xmax * image_np.shape[1]

    # Create a Rectangle patch
    rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='r', facecolor='none')

    if debug:
        # Add the patch to the Axes
        ax2.add_patch(rect)

# Get the number of people detected by the bounding boxes
N = len(people_boxes)

# Get total confidence score for each instance
total_confidence_scores = [np.sum(person[:, 2]) for person in keypoints_with_scores]

# Get indices of instances sorted by total confidence score
sorted_indices = np.argsort(total_confidence_scores)[::-1]

# Select the top N instances
selected_indices = sorted_indices[:N] 

selected_instances = []
for idx in sorted_indices:
    person = keypoints_with_scores[idx]
    overlaps = False
    for selected_person in selected_instances:
        # Get the bounding boxes for the current person and the selected person
        person_box = get_bounding_box(person)
        selected_person_box = get_bounding_box(selected_person)
        # Check if person overlaps with selected_person
        if check_overlap(person_box, selected_person_box):
            overlaps = True
            break
    if not overlaps:
        selected_instances.append(person)
    if len(selected_instances) == N:
        break

for person_idx, person in enumerate(selected_instances):
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
        height, width, _ = image_np.shape
        calculate_slope_and_annotate(ax2, midpoints_x_img, midpoints_y_img, person_idx, width, height)
        
        # Add a label at the position of the first keypoint
        head_keypoint_x = person[0][1] * width
        head_keypoint_y = person[0][0] * height
        fontsize = np.log(width) * 2
        ax2.text(head_keypoint_x, (head_keypoint_y - (height * (0.05))), f"{person_idx + 1}", color='green', fontsize=fontsize, ha='left', va='bottom', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
        
        
    # Plot a line connecting the midpoints
    ax2.plot(midpoints_x_img, midpoints_y_img, 'g-', linewidth=2)

# # Display the image on the axes
ax2.imshow(image_np)

ax1.axis('off')  # to remove axes
ax2.axis('off')  # to remove axes


# To save the image
fig2.savefig('output_with_midline.jpg', bbox_inches='tight', pad_inches=0)