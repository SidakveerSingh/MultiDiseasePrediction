import cv2
import numpy as np
from tensorflow import keras
import os

# Get the correct paths to the model and image (go up 2 levels to project root)
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(base_path, 'src', 'backend', 'models', 'lung_cancer_detection_model.keras')
image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpeg')

# Load model
model = keras.models.load_model(model_path)
print("✓ Model loaded")

# Test with the image
img = cv2.imread(image_path)
if img is None:
    print("Failed to read image")
else:
    print("Image shape:", img.shape)
    resized_img = cv2.resize(img, (64, 64))
    img_array = np.expand_dims(resized_img, axis=0)
    print("Processed array shape:", img_array.shape)

    predictions = model.predict(img_array)
    print("Predictions shape:", predictions.shape)
    print("Predictions:", predictions)

    predicted_idx = np.argmax(predictions[0])
    print("Predicted index:", predicted_idx)
    print("Predicted class:", ['colon_aca', 'colon_n', 'lung_aca', 'lung_n', 'lung_scc'][predicted_idx])