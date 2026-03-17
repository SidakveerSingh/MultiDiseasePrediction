"""Heart Disease Prediction Routes"""

import numpy as np
from flask import Blueprint, request, jsonify
import pickle
from config import (
    HEART_MODEL_PATH, HEART_FEATURES, DEFAULT_HEART_FEATURES,
    HEART_HIGH_RISK_THRESHOLD, HEART_MODERATE_RISK_THRESHOLD
)

heart_bp = Blueprint('heart', __name__, url_prefix='/api/heart')

# Load heart model
try:
    heart_model = pickle.load(open(HEART_MODEL_PATH, 'rb'))
except Exception as e:
    print(f"Error loading heart model: {e}")
    heart_model = None


def _parse_value(val, default):
    """Parse and validate numeric values."""
    try:
        if val is None or (isinstance(val, str) and val.strip() == ''):
            return default
        return float(val)
    except Exception:
        return default


def _sigmoid(x):
    """Sigmoid function for probability conversion."""
    return 1 / (1 + np.exp(-x))


def _compute_heart_risk_score(features):
    """
    Compute heuristic risk score based on medical factors.
    Used as fallback when model is unavailable.
    """
    score = 0.0

    age = features.get('age', DEFAULT_HEART_FEATURES['age'])
    score += max(0, (age - 40) / 40) * 2

    chol = features.get('chol', DEFAULT_HEART_FEATURES['chol'])
    score += max(0, (chol - 200) / 200) * 3

    trbps = features.get('trbps', DEFAULT_HEART_FEATURES['trbps'])
    score += max(0, (trbps - 120) / 120) * 2.5

    thalach = features.get('thalach', DEFAULT_HEART_FEATURES['thalach'])
    score += 0.5 if thalach < 120 else 0

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


def _get_risk_level(probability):
    """Determine risk level based on prediction probability."""
    if probability >= HEART_HIGH_RISK_THRESHOLD:
        return {
            'risk_level': 'High Risk',
            'advice': 'Please consult a healthcare provider as soon as possible.'
        }
    elif probability >= HEART_MODERATE_RISK_THRESHOLD:
        return {
            'risk_level': 'Moderate Risk',
            'advice': 'Consider lifestyle changes and follow up with a doctor.'
        }
    else:
        return {
            'risk_level': 'Low Risk',
            'advice': 'Keep up healthy habits and monitor regularly.'
        }


@heart_bp.route('/predict', methods=['POST'])
def predict_heart():
    """
    Predict heart disease risk based on patient features.
    
    Expected JSON:
    {
        "age": 54,
        "sex": 1,
        "cp": 0,
        "trbps": 130,
        ...
    }
    """
    try:
        data = request.get_json() or {}

        # Build feature dictionary with defaults
        used_fields = {}
        for feature in HEART_FEATURES:
            value = data.get(feature, None)
            used_fields[feature] = _parse_value(value, DEFAULT_HEART_FEATURES[feature])

        # Prepare features for model
        features = np.array(list(used_fields.values())).reshape(1, -1)

        # Get prediction
        if heart_model is not None:
            try:
                prediction = int(heart_model.predict(features)[0])
                probability = float(heart_model.predict_proba(features)[0][1])
            except Exception as e:
                print(f"Model prediction error: {e}, using fallback")
                score = _compute_heart_risk_score(used_fields)
                probability = float(_sigmoid(score / 4 - 1))
                prediction = int(probability >= 0.5)
        else:
            # Fallback to heuristic scoring
            score = _compute_heart_risk_score(used_fields)
            probability = float(_sigmoid(score / 4 - 1))
            prediction = int(probability >= 0.5)

        # Get risk level and advice
        risk_info = _get_risk_level(probability)

        return jsonify({
            'prediction': prediction,
            'confidence': probability,
            'risk_level': risk_info['risk_level'],
            'advice': risk_info['advice'],
            'used_features': used_fields
        }), 200

    except Exception as e:
        print(f"Error in predict_heart: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 400


@heart_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'Heart prediction service is running',
        'model_loaded': heart_model is not None
    }), 200
