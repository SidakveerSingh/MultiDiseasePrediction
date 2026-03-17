"""
MediScan - AI-Powered Disease Prediction Application
Main Flask Application
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
from routes.heart import heart_bp
from routes.lung import lung_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['JSON_SORT_KEYS'] = False

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register blueprints
app.register_blueprint(heart_bp)
app.register_blueprint(lung_bp)


@app.route('/health', methods=['GET'])
def health():
    """Main health check endpoint."""
    return jsonify({
        'status': 'MediScan API is running',
        'service': 'Multi-Disease Prediction',
        'endpoints': {
            'heart': '/api/heart/predict',
            'lung': '/api/lung/predict',
            'health': '/health'
        }
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        'app': 'MediScan',
        'description': 'AI-Powered Disease Prediction Application',
        'version': '1.0',
        'endpoints': {
            'health_check': 'GET /',
            'heart_prediction': 'POST /api/heart/predict',
            'lung_prediction': 'POST /api/lung/predict'
        },
        'info': 'Visit /health for service status'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found', 'status': 404}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error', 'status': 500}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("🏥 MediScan API Starting...")
    print("=" * 50)
    print("📍 Running on http://127.0.0.1:5000")
    print("🔗 Upload folder:", UPLOAD_FOLDER)
    print("📦 CORS enabled for frontend")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)