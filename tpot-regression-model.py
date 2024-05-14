# tpot-regression-model.py (do not change/remove this comment)
import pandas as pd
from joblib import load
import annotate

input_image = r"cropped\2024-05-14_23-54-01-0.jpg"

annotator = annotate.Annotator(input_image)
annotator.annotate_and_mask()
area = annotator.area()
average_length = annotator.length()
average_width = annotator.width()
perimeter = annotator.perimeter()

model_scaler = load(r'models\regression_model_scaler.joblib')
new_data = pd.DataFrame({'area': [area], 'length': [average_length], 'width': [average_width], 'perimeter': [perimeter]}, index=[0])
predicted_result = model_scaler.predict(new_data)

print(predicted_result[0])
