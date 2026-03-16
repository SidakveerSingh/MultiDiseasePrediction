from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
from tensorflow import keras

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load models
import pickle
heart_model = pickle.load(open('heart.pkl', 'rb'))
lung_model = None  # Lazy load

# Constants
HEART_FEATURES = ['age', 'sex', 'cp', 'trbps', 'chol', 'fbs', 'restecg', 
                  'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
LUNG_CLASSES = ['colon_aca', 'colon_n', 'lung_aca', 'lung_n', 'lung_scc']
IMG_SIZE = 64

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running'}), 200

# Default/typical feature values (used when a field is missing)
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


def _parse_value(val, default):
    try:
        if val is None or (isinstance(val, str) and val.strip() == ''):
            return default
        return float(val)
    except Exception:
        return default


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def _compute_heart_risk_score(features):
    # heuristic scoring based on commonly used risk factors
    score = 0.0

    age = features.get('age', DEFAULT_HEART_FEATURES['age'])
    score += max(0, (age - 40) / 40) * 2  # increased weight

    chol = features.get('chol', DEFAULT_HEART_FEATURES['chol'])
    score += max(0, (chol - 200) / 200) * 3  # increased weight

    trbps = features.get('trbps', DEFAULT_HEART_FEATURES['trbps'])
    score += max(0, (trbps - 120) / 120) * 2.5  # increased weight

    thalach = features.get('thalach', DEFAULT_HEART_FEATURES['thalach'])
    score += 0.5 if thalach < 120 else 0  # increased penalty

    score += 0.5 if features.get('fbs', DEFAULT_HEART_FEATURES['fbs']) == 1 else 0
    score += 0.6 if features.get('exang', DEFAULT_HEART_FEATURES['exang']) == 1 else 0

    cp = features.get('cp', DEFAULT_HEART_FEATURES['cp'])
    score += (cp / 3) * 0.8

    oldpeak = features.get('oldpeak', DEFAULT_HEART_FEATURES['oldpeak'])
    score += min(oldpeak / 4, 1) * 1.2

    ca = features.get('ca', DEFAULT_HEART_FEATURES['ca'])
    score += (ca / 3) * 0.9

    slope = features.get('slope', DEFAULT_HEART_FEATURES['slope'])
    score += 0.4 if slope == 2 else 0

    thal = features.get('thal', DEFAULT_HEART_FEATURES['thal'])
    score += 0.4 if thal == 3 else 0

    restecg = features.get('restecg', DEFAULT_HEART_FEATURES['restecg'])
    score += 0.2 if restecg == 2 else 0

    return score


@app.route('/predict-heart', methods=['POST'])
def predict_heart():
    try:
        data = request.get_json() or {}

        # Build feature dictionary and fill missing values with defaults
        used_fields = {}
        for f in HEART_FEATURES:
            value = data.get(f, None)
            used_fields[f] = _parse_value(value, DEFAULT_HEART_FEATURES[f])

        features = np.array(list(used_fields.values())).reshape(1, -1)

        # Use the trained model for prediction
        try:
            prediction = int(heart_model.predict(features)[0])
            probability = float(heart_model.predict_proba(features)[0][1])
        except Exception:
            # Fallback: use the heuristic scoring if model is not available
            score = _compute_heart_risk_score(used_fields)
            probability = float(_sigmoid(score / 4 - 1))
            prediction = int(probability >= 0.5)

        if probability >= 0.65:
            risk_level = 'High Risk'
            advice = 'Please consult a healthcare provider as soon as possible.'
        elif probability >= 0.3:
            risk_level = 'Moderate Risk'
            advice = 'Consider lifestyle changes and follow up with a doctor.'
        else:
            risk_level = 'Low Risk'
            advice = 'Keep up healthy habits and monitor regularly.'

        return jsonify({
            'risk_level': risk_level,
            'confidence': probability,
            'advice': advice,
            'used_features': used_fields
        })
    except Exception as e:
        print("Error in predict_heart:", str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/predict-lung', methods=['POST'])
def predict_lung():
    global lung_model
    print("Checking if model is loaded")
    if lung_model is None:
        print("Loading lung model")
        try:
            lung_model = keras.models.load_model('lung_cancer_detection_model.keras')
            print("Model loaded successfully")
        except Exception as e:
            print("Error loading model:", str(e))
            return jsonify({'error': 'Model loading failed: ' + str(e)}), 500
    try:
        print("Processing request")
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid image format'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("Image saved to", filepath)
        
        img = cv2.imread(filepath)
        if img is None:
            os.remove(filepath)
            return jsonify({'error': 'Invalid image file'}), 400
        print("Image read, shape:", img.shape)
        resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img_array = np.expand_dims(resized_img, axis=0)
        print("Image processed, array shape:", img_array.shape)
        
        predictions = lung_model.predict(img_array)
        print("Predictions:", predictions)
        predicted_idx = np.argmax(predictions[0])
        
        os.remove(filepath)
        
        return jsonify({
            'disease': LUNG_CLASSES[predicted_idx],
            'confidence': float(predictions[0][predicted_idx])
        })
    except Exception as e:
        print("Error in predict_lung:", str(e))
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)