# MediScan

MediScan is an advanced AI-powered application for predicting heart disease and lung cancer using machine learning models.

## Project Structure

MultiDiseasePrediction/
│
├── README.md
├── requirements.txt
├── REFACTORING_GUIDE.md
│
├── 📁 src/
│   ├── 📁 backend/
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── 📁 models/                    (ML Models)
│   │   │   ├── heart.pkl
│   │   │   └── lung_cancer_detection_model.keras
│   │   ├── 📁 routes/                    (API Routes)
│   │   │   ├── __init__.py
│   │   │   ├── heart.py
│   │   │   └── lung.py
│   │   └── 📁 uploads/                   (Auto-created for images)
│   │
│   └── 📁 frontend/                      (React App)
│       ├── package.json
│       ├── public/
│       │   └── index.html
│       └── src/
│           ├── App.js
│           ├── App.css
│           ├── index.js
│           └── index.css
│
├── 📁 training/
│   ├── Heart_Disease_Prediction.ipynb
│   ├── Lung-Cancer-Detection-using-CNN-V2.ipynb
│   │
│   ├── 📁 data/                         (NEW - Datasets folder)
│   │   ├── heart.csv                    (To download from Kaggle)
│   │   └── lung_images/                 (To download from Kaggle)
│   │
│   └── 📁 tests/                        (NEW - Test files)
│       ├── test_lung.py
│       ├── test_model.py
│       ├── test_real.py
│       └── test_image.jpeg
│
└── 📁 MDvenv/                           (Virtual environment)

## Setup

### 1. Environment
- Create a Python virtual environment:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows (PowerShell)
  venv\Scripts\activate.bat    # Windows (cmd)
  source venv/bin/activate # macOS/Linux

- Install dependencies:
  pip install -r requirements.txt

### Backend (Flask)

1. Navigate to the backend directory: `cd src\backend`
2. Run the Flask app: `python app.py`

The backend will run on http://localhost:5000

### Frontend (React)

1. In a seperate terminal, navigate to the frontend directory: `cd src\frontend`
2. Install dependencies: `npm install` (already done)
3. Start the React app: `npm start`

The frontend will run on http://localhost:3000

## Usage

- Open the frontend in your browser.
- Choose Heart Disease or Lung Cancer prediction.
- Fill the form and submit.
- Use the Back button to return to the main page.

## Models

- **Heart Disease**: Random Forest model trained on [heart.csv](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)
- **Lung Cancer**: CNN model trained on [Lung Cancer Imaging Dataset](<INSERT-KAGGLE-LINK-HERE>)

> Note: Datasets are not included in this repository due to size and licensing. Please download them from the provided links before running the training notebooks.  
> Place the dataset files inside:  
> ```
> MultiDiseasePrediction/training/data/
> ```