import cv2
import numpy as np
from tensorflow import keras
import os

# Get the correct path to the model (go up 2 levels to project root, then to src/backend/models/)
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(base_path, 'src', 'backend', 'models', 'lung_cancer_detection_model.keras')

# Load model
model = keras.models.load_model(model_path)
print("✓ Model loaded")

# Test with a dummy image or check the model
print("Model input shape:", model.input_shape)
print("Model output shape:", model.output_shape)

# Create a dummy image
dummy_img = np.random.rand(64, 64, 3) * 255
dummy_img = dummy_img.astype(np.uint8)
resized = cv2.resize(dummy_img, (64, 64))
img_array = np.expand_dims(resized, axis=0)
print("Dummy image shape:", img_array.shape)

predictions = model.predict(img_array)
print("Predictions shape:", predictions.shape)
print("Predictions:", predictions)

predicted_idx = np.argmax(predictions[0])
print("Predicted index:", predicted_idx)
print("Predicted class:", ['colon_aca', 'colon_n', 'lung_aca', 'lung_n', 'lung_scc'][predicted_idx])