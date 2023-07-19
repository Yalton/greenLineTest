import cv2
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
from scipy.stats import linregress

# Set the debug variable
debug = True

# def calculate_slope_and_annotate(image, midpoints_x, midpoints_y, person_idx):
#     if len(midpoints_x) >= 2 and len(midpoints_y) >= 2:
#         slope, intercept, r_value, p_value, std_err = linregress(midpoints_x, midpoints_y)
#         verticality_percentage = abs(slope) / (1 + abs(slope)) * 100
#         text = f"Chad Score: {verticality_percentage:.2f}%"
#         position = (30, 30 + person_idx * 50)
#         cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

def calculate_slope_and_annotate(image_np, midpoints_x, midpoints_y, person_idx):
    # Calculate the slope of the line using a linear regression
    if len(midpoints_x) >= 2 and len(midpoints_y)  >= 2: 
        slope, intercept, r_value, p_value, std_err = linregress(midpoints_x, midpoints_y)
        
        # Calculate the font scale and position based on the image's size
        font_scale = image_np.shape[1] / 1000  # Adjust the denominator to get the desired font size
        position = (int(image_np.shape[1] * 0.05), int(image_np.shape[0] * (0.1 + person_idx * 0.15)))

        # Draw text on image
        text = f"Slope: {slope:.2f}"
        cv2.putText(image_np, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 2, cv2.LINE_AA)


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
image = Image.open('image.jpg').convert('RGB')

# Convert the image to numpy array
image_np = np.array(image)

# Convert the image to the BGR format
image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

# Convert the image to the size the SSD MobileNet model expects and add a batch dimension
input_tensor = tf.convert_to_tensor(image_np)
input_tensor = input_tensor[tf.newaxis, ...]

# Run the image through the SSD MobileNet model
output_dict = ssd_mobilenet(input_tensor)

# The output is a dictionary with keys for 'detection_scores', 'detection_classes', and 'detection_boxes'
scores = output_dict['detection_scores'].numpy()[0]
classes = output_dict['detection_classes'].numpy()[0]
boxes = output_dict['detection_boxes'].numpy()[0]

# Resize the image to the size the model expects and add a batch dimension
image_resized = tf.image.resize(image_np, (384, 640))
image_resized = tf.expand_dims(image_resized, axis=0)

# Run the image through the model
outputs = movenet(tf.cast(image_resized, dtype=tf.int32))

# The output is a dictionary with a 'output_0' key that contains the pose keypoints
keypoints_with_scores = outputs['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))

# Scale the keypoints back to original image size
keypoints_with_scores[:,:,0] *= image_np.shape[0] / 384
keypoints_with_scores[:,:,1] *= image_np.shape[1] / 640

pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]

# Define a threshold for the detection score
score_threshold = 0.5

boxes_img_scale = boxes * [image_np.shape[0], image_np.shape[1], image_np.shape[0], image_np.shape[1]]

# Filter the bounding boxes based on the detection class and score
people_boxes = boxes_img_scale[(classes == 1) & (scores > score_threshold)]

# Get the number of people detected by the bounding boxes
N = len(people_boxes)

# Get total confidence score for each instance
total_confidence_scores = [np.sum(person[:, 2]) for person in keypoints_with_scores]

# Get indices of instances sorted by total confidence score
sorted_indices = np.argsort(total_confidence_scores)[::-1]

# Select the top N instances
selected_indices = sorted_indices[:N]

print(f"Number of people detected {N}")
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

print(f"Selected instances: {selected_instances}")
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
            print(f'Midpoints: ({midpoint_x}, {midpoint_y})')  # Print midpoints
            
            # Print keypoint coordinates
            print(f'Keypoint coordinates: ({person[i][0]}, {person[i][1]}), ({person[j][0]}, {person[j][1]})')
        else:
            # If the keypoint confidence scores are not greater than the threshold, print them
            print(f'Keypoint confidence scores: ({person[i][2]}, {person[j][2]})')

    # Print person keypoints and scores
    print(f'Person keypoints and scores: {person}')

    # Calculate slope and annotate image
    if midpoints_x and midpoints_y:
        calculate_slope_and_annotate(image_np, midpoints_x, midpoints_y, person_idx)

if debug:
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

        # Draw keypoints
        for point in person:
            cv2.circle(image_np, (int(point[1]), int(point[0])), 5, (255, 0, 0), -1)

        # Draw midpoints
        for mid_x, mid_y in zip(midpoints_x, midpoints_y):
            cv2.circle(image_np, (int(mid_x), int(mid_y)), 5, (0, 255, 0), -1)

        # Draw midline
        for i in range(len(midpoints_x) - 1):
            cv2.line(image_np, (int(midpoints_x[i]), int(midpoints_y[i])),
                     (int(midpoints_x[i + 1]), int(midpoints_y[i + 1])), (0, 255, 0), 2)

        # Get bounding box for the person
        person_box = get_bounding_box(person)

        # Draw the bounding box on the image
        cv2.rectangle(image_np, (int(person_box[1]), int(person_box[0])), (int(person_box[3]), int(person_box[2])), (0, 255, 0), 2)

# Save the image
cv2.imwrite('neo_output_with_midline.jpg', image_np)
