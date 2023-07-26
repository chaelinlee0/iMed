from flask import Flask, render_template, redirect, url_for, request, jsonify
import json
import re
import ast
import os
import openai
from dotenv import load_dotenv
from ML.disease_classifier import DiseaseClassifier
from flask_cors import CORS

disease_classifier = DiseaseClassifier()
disease_classifier.train_model()

load_dotenv()
api_key = os.getenv('OPEN_API_KEY')
openai.api_key = api_key

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "*"])

@app.route('/')
def start():
    return "Hello World!"


@app.route('/api/process_data/')
def get_disease():
    def extract_array(s):
        array_pattern = r'\[.*?\]'
        array_string = re.search(array_pattern, s)
        if array_string:
            try:
                return ast.literal_eval(array_string.group(0))
            except (ValueError, SyntaxError):
                return None
        else:
            return None

    input_value = request.args.get('input')
    data = {'message': input_value + ' ' + str(len(input_value))}
    features = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
    input = f'Here is your feature array: {features} \Return an array of strings of the actual features indicated by the symptoms of a patient with the following description{input_value}'

    response = openai.ChatCompletion.create(
            messages = [ 
                {"role": "user", "content": input}],
            model="gpt-3.5-turbo",
        ) 
    text = response.choices[0].message.content
    arr = extract_array(text)
    if arr is None:
        return jsonify({'disease': 'No disease found'}) 
    symptoms = [1 if feature in arr else 0 for feature in features]
    disease = disease_classifier.predict(symptoms)
    ret = {'disease': disease}
    ret_as_list = {key: value.tolist() for key, value in ret.items()}
    return json.dumps(ret_as_list)

if __name__ == "__main__":
    app.run(debug=True)
    pass

 