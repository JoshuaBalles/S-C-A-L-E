import pandas as pd
from joblib import load

# Load the trained model and scaler
model_scaler = load('model_scaler.joblib')

# Create a DataFrame from the individual feature values
new_data = pd.DataFrame({'area': [97009], 'length': [596.42], 'width': [178.02], 'perimeter': [1846.31]})

# Predict using the loaded model and scaler
predicted_result = model_scaler.predict(new_data)

print(predicted_result)
