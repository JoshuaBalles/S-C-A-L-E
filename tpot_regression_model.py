# tpot_regression_model.py (do not change/remove this comment)
import pandas as pd
from joblib import load
import annotate

def predict_from_image(input_image_path):
    # Initialize annotator
    annotator = annotate.Annotator(input_image_path)
    annotator.annotate_and_mask()

    # Extract features
    area = annotator.area()
    average_length = annotator.length()
    average_width = annotator.width()
    perimeter = annotator.perimeter()

    # Load model scaler
    model_scaler = load(r'models\regression_model_scaler.joblib')

    # Create DataFrame for new data
    new_data = pd.DataFrame({'area': [area], 'length': [average_length], 'width': [average_width], 'perimeter': [perimeter]}, index=[0])

    # Predict using the model scaler
    predicted_result = model_scaler.predict(new_data)

    return predicted_result[0]