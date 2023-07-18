from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import tensorflow_hub as hub
import base64
import io
from PIL import Image
import numpy as np

app = FastAPI()

# Load the pose estimation model from TensorFlow Hub
model = hub.load('https://tfhub.dev/google/movenet/singlepose/lightning/1')

class Item(BaseModel):
    base64_image: str

@app.post("/predict")
def predict(item: Item):
    # Decode the base64 image
    base64_image = item.base64_image
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes))

    # Preprocess the image so it can be fed into the model
    # Convert the image to numpy array
    image = np.array(image)
    # Normalize the image to the range [0, 1]
    image = image / 255.0
    # Resize the image to the size the model expects
    image = tf.image.resize(image, (192, 192))
    # Add a batch dimension
    image = tf.expand_dims(image, axis=0)

    # Run the image through the model
    outputs = model(image)

    # The output is a dictionary with a 'output_0' key that contains the pose keypoints
    keypoints = outputs['output_0'].numpy()[0]

    # Return the keypoints
    return {"keypoints": keypoints.tolist()}
