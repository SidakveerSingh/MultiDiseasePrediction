"""Configuration settings for the MediScan backend."""

import os

# Flask Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Model Paths
MODELS_FOLDER = 'models'
HEART_MODEL_PATH = os.path.join(MODELS_FOLDER, 'heart.pkl')
LUNG_MODEL_PATH = os.path.join(MODELS_FOLDER, 'lung_cancer_detection_model.keras')

# Image Processing
IMG_SIZE = 64

# Heart Disease Features
HEART_FEATURES = [
    'age', 'sex', 'cp', 'trbps', 'chol', 'fbs', 'restecg',
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

DEFAULT_HEART_FEATURES = {
    'age': 54,
    'sex': 1,
    'cp': 0,
    'trbps': 130,
    'chol': 246,
    'fbs': 0,
    'restecg': 1,
    'thalach': 150,
    'exang': 0,
    'oldpeak': 1.0,
    'slope': 1,
    'ca': 0,
    'thal': 2
}

# Lung Cancer Classes
LUNG_CLASSES = ['colon_aca', 'colon_n', 'lung_aca', 'lung_n', 'lung_scc']

# Risk Level Thresholds
HEART_HIGH_RISK_THRESHOLD = 0.65
HEART_MODERATE_RISK_THRESHOLD = 0.3
