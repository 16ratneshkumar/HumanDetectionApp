from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import cv2
import json
import base64
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# Load your model here (example placeholder)
# model = load_your_model_function()
model = tf.keras.models.load_model('./detector/human_detection_model.keras')
img_height, img_width = 224, 224

def model_predict(image):
    resized_frame = cv2.resize(image, (img_height, img_width))
    img_array = np.expand_dims(resized_frame, axis=0)
    img_array = preprocess_input(img_array)
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5 : # Returns True if human is detected
        result = "Human Detected!"  # Placeholder result
    else:
        result = " No Human Detected!"  # Placeholder result
    return result
    # Placeholder function for model prediction
    # Replace with actual model inference
    # result = model.predict(image)
    

def home(request):
    return render(request, 'home.html')

def detect(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request.body
            data = json.loads(request.body)
            image_data = data.get('image')

            if image_data:
                # Decode the base64 image
                image_data = image_data.split(",")[1]  # Remove the prefix
                img_bytes = base64.b64decode(image_data)
                img = Image.open(io.BytesIO(img_bytes))
                img = np.array(img)

                # Convert image to BGR for OpenCV
                if img.shape[2] == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                # Perform model prediction
                result = model_predict(img)
                return JsonResponse({"result": result})

        except Exception as e:
            print("Error in processing image:", e)
            return JsonResponse({"error": "Failed to process image"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)