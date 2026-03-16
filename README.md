# MediScan

MediScan is an advanced AI-powered application for predicting heart disease and lung cancer using machine learning models.

## Setup

### Backend (Flask)

1. Navigate to the backend directory: `cd backend`
2. Run the Flask app: `python app.py`

The backend will run on http://localhost:5000

### Frontend (React)

1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install` (already done)
3. Start the React app: `npm start`

The frontend will run on http://localhost:3000

## Usage

- Open the frontend in your browser.
- Choose Heart Disease or Lung Cancer prediction.
- Fill the form and submit.
- Use the Back button to return to the main page.

## Models

- Heart Disease: Random Forest model trained on heart.csv
- Lung Cancer: CNN model for image classification