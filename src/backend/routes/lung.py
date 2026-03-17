"""Lung Cancer Detection Routes"""

import cv2
import numpy as np
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow import keras
from config import (
    UPLOAD_FOLDER, ALLOWED_EXTENSIONS, LUNG_MODEL_PATH,
    LUNG_CLASSES, IMG_SIZE
)

lung_bp = Blueprint('lung', __name__, url_prefix='/api/lung')

# Global variable for lazy-loaded model
lung_model = None


def allowed_file(filename):
    """Check if uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _load_lung_model():
    """Load the lung cancer detection model."""
    global lung_model
    if lung_model is None:
        try:
            lung_model = keras.models.load_model(LUNG_MODEL_PATH)
            print("✓ Lung model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading lung model: {e}")
            raise
    return lung_model


def _preprocess_image(filepath):
    """
    Preprocess image for model input.
    
    Args:
        filepath: Path to image file
        
    Returns:
        Preprocessed image array or None if error
    """
    img = cv2.imread(filepath)
    if img is None:
        return None
    
    # Resize to model input size
    resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    
    # Add batch dimension
    img_array = np.expand_dims(resized_img, axis=0)
    
    return img_array


def _get_prediction_confidence(predictions):
    """
    Extract most confident prediction.
    
    Args:
        predictions: Model output array
        
    Returns:
        Tuple of (disease_class, confidence)
    """
    predicted_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_idx])
    disease = LUNG_CLASSES[predicted_idx]
    
    return disease, confidence


@lung_bp.route('/predict', methods=['POST'])
def predict_lung():
    """
    Predict lung cancer from uploaded image.
    
    Expected: Multipart form with 'image' field containing JPEG/PNG file
    """
    global lung_model
    
    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Check filename
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file format. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Create uploads folder if needed
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"✓ Image saved: {filepath}")
        
        # Load model
        try:
            _load_lung_model()
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Model loading failed: {str(e)}'}), 500
        
        # Preprocess image
        img_array = _preprocess_image(filepath)
        if img_array is None:
            os.remove(filepath)
            return jsonify({'error': 'Invalid or corrupt image file'}), 400
        
        print(f"✓ Image preprocessed, shape: {img_array.shape}")
        
        # Make prediction
        predictions = lung_model.predict(img_array)
        print(f"✓ Model prediction: {predictions}")
        
        # Extract results
        disease, confidence = _get_prediction_confidence(predictions)
        
        # Clean up uploaded file
        os.remove(filepath)
        print(f"✓ Temporary file removed")
        
        return jsonify({
            'disease': disease,
            'confidence': confidence,
            'message': 'Prediction successful'
        }), 200
        
    except Exception as e:
        print(f"✗ Error in predict_lung: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


@lung_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'Lung cancer detection service is running',
        'model_loaded': lung_model is not None,
        'supported_formats': list(ALLOWED_EXTENSIONS)
    }), 200


# Create uploads folder on route initialization
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
