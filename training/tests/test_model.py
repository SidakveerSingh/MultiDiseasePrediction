import pickle
import numpy as np
import os

# Get the correct path to the model (go up 2 levels to project root, then to src/backend/models/)
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(base_path, 'src', 'backend', 'models', 'heart.pkl')

model = pickle.load(open(model_path, 'rb'))
print('✓ Model loaded')

# Test with some features - high risk example
test_features = np.array([[45, 1, 3, 150, 300, 1, 2, 120, 1, 2.5, 2, 2, 3]])
pred = model.predict(test_features)
prob = model.predict_proba(test_features)
print('Test prediction:', pred[0])
print('Test probabilities:', prob[0])

# Test with low risk example
low_risk = np.array([[30, 0, 0, 120, 200, 0, 0, 180, 0, 0, 0, 0, 1]])
pred2 = model.predict(low_risk)
prob2 = model.predict_proba(low_risk)
print('Low risk prediction:', pred2[0])
print('Low risk probabilities:', prob2[0])