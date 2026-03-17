import React from 'react';
import { Route, BrowserRouter as Router, Routes, useNavigate } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/heart" element={<Heart />} />
          <Route path="/lung" element={<Lung />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  const navigate = useNavigate();
  return (
    <div className="home">
      <div className="hero">
        <h1>Welcome to MediScan</h1>
        <p className="subtitle">Advanced AI-powered predictions for heart disease and lung cancer detection</p>
        <p className="description">Select the type of prediction you want to perform:</p>
        <div className="button-container">
          <button className="choice-btn heart-btn" onClick={() => navigate('/heart')}>
            ❤️ Heart Disease Prediction
          </button>
          <button className="choice-btn lung-btn" onClick={() => navigate('/lung')}>
            🫁 Lung Cancer Prediction
          </button>
        </div>
      </div>
    </div>
  );
}

function Heart() {
  const navigate = useNavigate();
  const [formData, setFormData] = React.useState({
    age: '', sex: '', cp: '', trbps: '', chol: '', fbs: '', restecg: '',
    thalach: '', exang: '', oldpeak: '', slope: '', ca: '', thal: ''
  });
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleReset = () => {
    setFormData({
      age: '', sex: '', cp: '', trbps: '', chol: '', fbs: '', restecg: '',
      thalach: '', exang: '', oldpeak: '', slope: '', ca: '', thal: ''
    });
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {};
      Object.entries(formData).forEach(([key, value]) => {
        if (value !== '' && value !== null && value !== undefined) {
          payload[key] = value;
        }
      });

      const response = await fetch('http://localhost:5000/api/heart/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: 'Failed to get prediction' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>❤️ Heart Disease Prediction</h2>
      <p style={{marginBottom: '18px', fontSize: '0.95rem', color: '#555'}}>
        You can fill in as many fields as you like. Missing values will be filled using typical defaults.
      </p>
      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <label title="Patient's age in years">Age: <input name="age" placeholder="e.g., 45" value={formData.age} onChange={handleChange} type="number" min="1" max="120" /></label>
          <label title="Biological sex: 0 for Female, 1 for Male">Sex: <select name="sex" value={formData.sex} onChange={handleChange}>
            <option value="">Select</option>
            <option value="0">Female</option>
            <option value="1">Male</option>
          </select></label>
          <label title="Chest pain type: 0=Typical Angina, 1=Atypical Angina, 2=Non-anginal Pain, 3=Asymptomatic">Chest Pain Type: <select name="cp" value={formData.cp} onChange={handleChange}>
            <option value="">Select</option>
            <option value="0">Typical Angina</option>
            <option value="1">Atypical Angina</option>
            <option value="2">Non-anginal Pain</option>
            <option value="3">Asymptomatic</option>
          </select></label>
          <label title="Resting blood pressure in mmHg">Resting Blood Pressure: <input name="trbps" placeholder="e.g., 130 mmHg" value={formData.trbps} onChange={handleChange} type="number" min="80" max="200" /></label>
          <label title="Serum cholesterol in mg/dl">Cholesterol: <input name="chol" placeholder="e.g., 200 mg/dl" value={formData.chol} onChange={handleChange} type="number" min="100" max="600" /></label>
          <label title="Fasting blood sugar > 120 mg/dl: 0=No, 1=Yes">Fasting Blood Sugar: <select name="fbs" value={formData.fbs} onChange={handleChange}>
            <option value="">Select</option>
            <option value="0">≤ 120 mg/dl</option>
            <option value="1">greater than 120 mg/dl</option>
          </select></label>
          <label title="Resting electrocardiographic results: 0=Normal, 1=ST-T Wave Abnormality, 2=Left Ventricular Hypertrophy">Resting ECG: <select name="restecg" value={formData.restecg} onChange={handleChange}>
            <option value="">Select</option>
            <option value="0">Normal</option>
            <option value="1">ST-T Wave Abnormality</option>
            <option value="2">Left Ventricular Hypertrophy</option>
          </select></label>
          <label title="Maximum heart rate achieved in bpm">Max Heart Rate: <input name="thalach" placeholder="e.g., 150 bpm" value={formData.thalach} onChange={handleChange} type="number" min="60" max="220" /></label>
          <label title="Exercise induced angina: 0=No, 1=Yes">Exercise Induced Angina: <select name="exang" value={formData.exang} onChange={handleChange}>
            <option value="">Select</option>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select></label>
          <label title="ST depression induced by exercise relative to rest">ST Depression: <input name="oldpeak" placeholder="e.g., 1.0" value={formData.oldpeak} onChange={handleChange} type="number" step="0.1" min="0" max="10" /></label>
          <label title="Slope of the peak exercise ST segment: 0=Upsloping, 1=Flat, 2=Downsloping">Slope: <select name="slope" value={formData.slope} onChange={handleChange}>
            <option value="">Select</option>
            <option value="0">Upsloping</option>
            <option value="1">Flat</option>
            <option value="2">Downsloping</option>
          </select></label>
          <label title="Number of major vessels colored by fluoroscopy (0-3)">Number of Major Vessels: <input name="ca" placeholder="0-3" value={formData.ca} onChange={handleChange} type="number" min="0" max="3" /></label>
          <label title="Thalassemia: 1=Normal, 2=Fixed Defect, 3=Reversible Defect">Thalassemia: <select name="thal" value={formData.thal} onChange={handleChange}>
            <option value="">Select</option>
            <option value="1">Normal</option>
            <option value="2">Fixed Defect</option>
            <option value="3">Reversible Defect</option>
          </select></label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? <><span className="loading"></span>Analyzing...</> : '🔍 Predict Heart Disease Risk'}
        </button>
        <button type="button" onClick={handleReset} className="reset-btn">🔄 Reset Form</button>
      </form>
      {result && (
        <div className={`result ${result.error ? '' : (result.risk_level === 'High Risk' ? 'high-risk' : result.risk_level === 'Moderate Risk' ? 'moderate-risk' : 'low-risk')}`}>
          {result.error ? <p>❌ Error: {result.error}</p> : (
            <>
              <h3>
                {result.risk_level === 'High Risk' ? '⚠️ High Risk Detected' : result.risk_level === 'Moderate Risk' ? '⚠️ Moderate Risk' : '✅ Low Risk'}
              </h3>
              <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
              <p>{result.advice || 'Based on the data provided, this is the predicted risk level.'}</p>
            </>
          )}
        </div>
      )}
      <button className="back-btn" onClick={() => navigate('/')}>⬅️ Back to Home</button>
    </div>
  );
}

function Lung() {
  const navigate = useNavigate();
  const [file, setFile] = React.useState(null);
  const [imagePreview, setImagePreview] = React.useState(null);
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => setImagePreview(e.target.result);
      reader.readAsDataURL(selectedFile);
    } else {
      setImagePreview(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);
    try {
      const response = await fetch('http://localhost:5000/api/lung/predict', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: 'Failed to get prediction' });
    } finally {
      setLoading(false);
    }
  };

  const getDiseaseEmoji = (disease) => {
    const emojis = {
      'colon_aca': '🫀',
      'colon_n': '✅',
      'lung_aca': '🫁',
      'lung_n': '✅',
      'lung_scc': '🫁'
    };
    return emojis[disease] || '🔍';
  };

  const getDiseaseName = (disease) => {
    const names = {
      'colon_aca': 'Colon Adenocarcinoma',
      'colon_n': 'Normal Colon Tissue',
      'lung_aca': 'Lung Adenocarcinoma',
      'lung_n': 'Normal Lung Tissue',
      'lung_scc': 'Lung Squamous Cell Carcinoma'
    };
    return names[disease] || disease;
  };

  return (
    <div className="form-container">
      <h2>🫁 Lung Cancer Detection</h2>
      <form onSubmit={handleSubmit}>
        <label>Upload Lung Image (JPEG/PNG): 
          <input type="file" accept="image/*" onChange={handleFileChange} required />
        </label>
        {imagePreview && (
          <div className="image-preview">
            <h3>📸 Image Preview</h3>
            <img src={imagePreview} alt="Uploaded lung image" />
          </div>
        )}
        <button type="submit" disabled={loading || !file}>
          {loading ? <><span className="loading"></span>Analyzing Image...</> : '🔬 Detect Lung Cancer'}
        </button>
      </form>
      {result && (
        <div className="result lung-result">
          {result.error ? <p>❌ Error: {result.error}</p> : (
            <>
              <h3>{getDiseaseEmoji(result.disease)} Detection Result</h3>
              <p><strong>Disease:</strong> {getDiseaseName(result.disease)}</p>
              <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
              {imagePreview && (
                <div className="image-preview">
                  <h4>📊 Analyzed Image</h4>
                  <img src={imagePreview} alt="Analyzed lung image" />
                </div>
              )}
              <p style={{marginTop: '10px', fontSize: '0.9rem'}}>
                {result.disease.includes('n') ? '✅ No abnormalities detected.' : '⚠️ Abnormalities detected. Please consult a medical professional for confirmation.'}
              </p>
            </>
          )}
        </div>
      )}
      <button className="back-btn" onClick={() => navigate('/')}>⬅️ Back to Home</button>
    </div>
  );
}

export default App;