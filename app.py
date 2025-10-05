from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the saved model
with open('employee_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Home Page
@app.route('/')
def home():
    return render_template('Home.html')

# About Page
@app.route('/about')
def about():
    return render_template('About.html')

# Predict Form Page
@app.route('/predict', methods=['GET'])
def predict_form():
    return render_template('predict.html')

# Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit():

        # Extract all 13 input values in exact order
    quarter = request.form['quarter']
    department = request.form['department']
    day = request.form['day']
    team = request.form['team']
    targeted_productivity = request.form['targeted_productivity']
    smv = request.form['smv']
    over_time = request.form['over_time']
    incentive = request.form['incentive']
    idle_time = request.form['idle_time']
    idle_men = request.form['idle_men']
    no_of_style_change = request.form['no_of_style_change']
    no_of_workers = request.form['no_of_workers']
    month = request.form['month']

    total = [[
        int(quarter), int(department), int(day), int(team),
        float(targeted_productivity), float(smv), int(over_time), int(incentive),
        float(idle_time), int(idle_men), int(no_of_style_change), float(no_of_workers),
        int(month)
    ]]

    prediction = model.predict(total)[0]  # Get scalar from array
    print("Prediction value:", prediction)

    if prediction < 0.3:
        text = 'The employee is averagely productive.'
    elif prediction <= 0.8:
        text = 'The employee is medium productive.'
    else:
        text = 'The employee is highly productive.'

    return render_template('Submit.html', prediction_text=f"{text}")


if __name__ == '__main__':
    app.run(debug=True)
