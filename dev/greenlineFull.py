# Your existing imports, plus some additional ones
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.stats import linregress
from skimage.transform import resize
import matplotlib.patches as patches


def draw_keypoints(frame, keypoints):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))

    for kp in shaped:
        ky, kx, kp_conf = kp
        # if kp_conf > confidence_threshold:
        cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)

def calculate_slope_and_annotate(image_np, midpoints_x, midpoints_y, person_idx):
    # Calculate the slope of the line using a linear regression
    if len(midpoints_x) >= 2 and len(midpoints_y)  >= 2: 
        slope, intercept, r_value, p_value, std_err = linregress(midpoints_x, midpoints_y)
        
        # Draw text on image
        text = f"Slope: {slope:.2f}"
        position = (30, 30 + person_idx * 50)
        ax.text(position[0], position[1], text, color='red', fontsize=12, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Load the SSD MobileNet model from TensorFlow Hub
ssd_mobilenet = hub.load('https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2')

# Load the MoveNet single pose model from TensorFlow Hub
movenet = hub.load('https://tfhub.dev/google/movenet/singlepose/lightning/1').signatures['serving_default']

# Load the image
image = Image.open('image1.jpg').convert('RGB')

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

# Define a threshold for the detection score
threshold = 0.5

# Define the class ID for 'person' in the COCO dataset
person_class_id = 1

# Create a figure and axes
fig, ax = plt.subplots()

# Display the image on the axes
ax.imshow(image_np)

# Define pairs of keypoints
pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]



fig1, ax1 = plt.subplots()  # create a new figure with its own axes for person detection
ax1.imshow(image_np)

# Loop over the detections
for idx, (score, cls, box) in enumerate(zip(scores, classes, boxes)):
    if score > threshold and cls == person_class_id:
        # The box is defined as [y_min, x_min, y_max, x_max], so we need to adjust the order
        box = [box[1], box[0], box[3], box[2]]

        # The box coordinates are normalized, so we need to convert them back to the original image size
        box = [int(b * dim) for b, dim in zip(box, (image_np.shape[1], image_np.shape[0], image_np.shape[1], image_np.shape[0]))]

        rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], linewidth=1, edgecolor='r', facecolor='none')
        ax1.add_patch(rect)

        # Crop the image to the bounding box
        cropped_image = image_np[box[1]:box[3], box[0]:box[2]]

        # Calculate the aspect ratio of the cropped image
        aspect_ratio = cropped_image.shape[1] / cropped_image.shape[0]

        # Calculate the padding to be added to the shorter side
        padding = (max(cropped_image.shape) - min(cropped_image.shape)) // 2

        # Pad the image to maintain the aspect ratio
        if aspect_ratio > 1:
            # If width > height, add padding to the top and bottom
            padded_image = np.pad(cropped_image, ((padding, padding), (0, 0), (0, 0)), mode='constant')
        elif aspect_ratio < 1:
            # If height > width, add padding to the left and right
            padded_image = np.pad(cropped_image, ((0, 0), (padding, padding), (0, 0)), mode='constant')
        else:
            padded_image = cropped_image

        # Calculate the scale factors for the x and y coordinates
        x_scale = padded_image.shape[1] / 192
        y_scale = padded_image.shape[0] / 192

        # Resize the padded image to the size the MoveNet model expects
        resized_image = resize(padded_image, (192, 192))

        # Add a batch dimension
        resized_image = tf.expand_dims(resized_image, axis=0)

        # Rescale the image values back to the 0-255 range
        resized_image = resized_image * 255

        # Run the resized image through the MoveNet model
        outputs = movenet(tf.cast(resized_image, dtype=tf.int32))

        # The output is a dictionary with a 'output_0' key that contains the pose keypoints
        keypoints_with_scores = outputs['output_0'].numpy()[0]

        # Adjust the keypoint coordinates to account for the bounding box and the padding
        keypoints_with_scores[:, :, 0] = keypoints_with_scores[:, :, 0] * x_scale + box[0]
        keypoints_with_scores[:, :, 1] = keypoints_with_scores[:, :, 1] * y_scale + box[1]



        print(keypoints_with_scores)
        print("Shape of Image: ", image_np.shape)
        print("Shape of keypoints_with_scores: ", keypoints_with_scores.shape)

        midpoints_x = []
        midpoints_y = []
        draw_keypoints(image_np, keypoints_with_scores)

        # For each pair of keypoints, calculate the midpoint and add it to the lists
        for i, j in pairs:
            midpoint_x = (keypoints_with_scores[0, i, 1] + keypoints_with_scores[0, j, 1]) / 2
            midpoint_y = (keypoints_with_scores[0, i, 0] + keypoints_with_scores[0, j, 0]) / 2
            midpoints_x.append(midpoint_x)
            midpoints_y.append(midpoint_y)

        # Transform midpoints back to original image's coordinates
        # midpoints_x = [mx * (box[2] - box[0]) + box[0] for mx in midpoints_x]
        # midpoints_y = [my * (box[3] - box[1]) + box[1] for my in midpoints_y]

        # Calculate slope and annotate image
        if midpoints_x and midpoints_y: 
            calculate_slope_and_annotate(image_np, midpoints_x, midpoints_y, idx)
        
        # Plot a line connecting the midpoints
        ax.plot(midpoints_x, midpoints_y, 'g-')
        
fig1.savefig('output_with_person_detection.jpg', bbox_inches='tight', pad_inches=0)


# Display the image on the axes
ax.imshow(image_np)

ax.axis('off')  # to remove axes
plt.show()

# To save the image
fig.savefig('output_with_midline.jpg', bbox_inches='tight', pad_inches=0)