from flask import Flask, render_template, request, url_for
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('building_height_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = {
        'Soil Type': [request.form['soil']],
        'Moisture (%)': [float(request.form['moisture'])],
        'Clay (%)': [float(request.form['clay'])],
        'Sand (%)': [float(request.form['sand'])],
        'Silt (%)': [float(request.form['silt'])],
        'pH': [float(request.form['ph'])],
        'Bearing Capacity (kPa)': [float(request.form['bc'])]
    }
    df = pd.DataFrame(input_data)
    prediction = model.predict(df)[0]
    floors = round(prediction / 3)
    result = (f"Predicted Height: {prediction:.2f} meters (~{floors} floors)")
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
