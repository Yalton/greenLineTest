import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

# Load the SSD MobileNet model from TensorFlow Hub
model = hub.load('https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2')

# Load the image
image_np = cv2.imread('IMG_1610.jpg')

# Convert the image to RGB
image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

# Convert the image to the size the model expects and add a batch dimension
input_tensor = tf.convert_to_tensor(image_rgb)
input_tensor = input_tensor[tf.newaxis,...]

# Run the image through the model
output_dict = model(input_tensor)

# The output is a dictionary with keys for 'detection_scores', 'detection_classes', and 'detection_boxes'
scores = output_dict['detection_scores'].numpy()[0]
classes = output_dict['detection_classes'].numpy()[0]
boxes = output_dict['detection_boxes'].numpy()[0]

# Define a threshold for the detection score
threshold = 0.5

# Define the class ID for 'person' in the COCO dataset
person_class_id = 1

# Loop over the detections
for score, cls, box in zip(scores, classes, boxes):
    if score > threshold and cls == person_class_id:
        # The box is defined as [y_min, x_min, y_max, x_max], so we need to adjust the order
        box = [box[1], box[0], box[3], box[2]]

        # The box coordinates are normalized, so we need to convert them back to the original image size
        box = [int(b * dim) for b, dim in zip(box, (image_np.shape[1], image_np.shape[0], image_np.shape[1], image_np.shape[0]))]

        # Draw the bounding box on the image
        cv2.rectangle(image_np, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

# Show the image
if cv2.imwrite('output_with_boxes.jpg', image_np):
    print("Image saved successfully")
else:
    print("Error saving image")
