# Use an official TensorFlow runtime as a parent image
FROM tensorflow/tensorflow:2.10.0-gpu

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx

# Install NVIDIA PyPI index and NVIDIA TensorRT
RUN pip install --no-cache-dir nvidia-pyindex
RUN pip install --no-cache-dir nvidia-tensorrt

# Install any needed packages specified in requirements.txt
RUN sed '/nvidia/d' requirements.txt > requirements_no_nvidia.txt
RUN pip install --no-cache-dir -r requirements_no_nvidia.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
