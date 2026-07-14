from flask import Flask, render_template, request, make_response
import pandas as pd
from flask import session
from flask import make_response, session
from google import genai
import csv
import os
import smtplib
from email.mime.text import MIMEText
client = genai.Client(api_key=YOUR_API_KEY)
app = Flask(__name__)
app.secret_key = "YOUR_SECRET_PASS"  # Required for session management
disease_df = pd.read_csv("datasets/Disease_Main_Table_intern.csv")
print(disease_df.columns.tolist())
body_df = pd.read_csv("datasets/Body_Systems_Dataset_intern.csv")
symptoms_df = pd.read_csv("datasets/Symptoms_Dataset_Diseases_intern.csv")
diagnosis_df = pd.read_csv("datasets/Diagnosis_Dataset_Diseases_intern.csv")
medicine_df = pd.read_csv("datasets/Medicine_Dataset_Diseases_intern.csv")
diet_df = pd.read_csv("datasets/Diet_Dataset_Diseases_intern.csv")
exercise_df = pd.read_csv("datasets/Exercise_Yoga_Dataset_Diseases_intern.csv")
prevention_df = pd.read_csv("datasets/Prevention_Dataset_Diseases_intern.csv")
emergency_df = pd.read_csv("datasets/Emergency_Dataset_Diseases_intern.csv")
primary_treatment_df = pd.read_csv("datasets/Primary_Treatment_Dataset_Diseases_intern.csv")
supportive_treatment_df = pd.read_csv("datasets/Supportive_Treatment_Dataset_Diseases_Intern.csv")

@app.route("/")
def home():    
    return render_template("dashboard.html")

@app.route("/brain-nervous")
def brain_nervous():
    return render_template("brain-nervous.html")

@app.route("/lungs")
def lungs():
    return render_template("lungs.html")

@app.route("/liver")
def liver():
    return render_template("liver.html")

@app.route("/heart-vascular")
def heart_vascular():
    return render_template("heart-vascular.html")

@app.route("/digestive-system")
def digestive_system():
    return render_template("digestive-system.html")

@app.route("/kidneys")
def kidneys():
    return render_template("kidneys.html")

@app.route("/skin")
def skin():
    return render_template("skin.html")

@app.route("/eyes")
def eyes():
    return render_template("eyes.html")

@app.route("/ears")
def ears():
    return render_template("ears.html")

@app.route("/reproductive-system")
def reproductive_system():
    return render_template("reproductive-system.html")

@app.route("/endocrine")
def endocrine():
    return render_template("endocrine.html")

@app.route("/bones-joints")
def bones_joints():
    return render_template("bones-joints.html")

@app.route("/modern-medicine")
def modern_medicine():
    return render_template("modern-medicine.html")


@app.route("/ayurveda")
def ayurveda():
    
    return render_template("ayurveda.html")


@app.route("/siddha")
def siddha():
    return render_template("siddha.html")


@app.route("/yoga-therapy")
def yoga():
    return render_template("yoga-therapy.html")


@app.route("/homeopathy")
def homeopathy():
    return render_template("homeopathy.html")


@app.route("/naturopathy")
def naturopathy():
    return render_template("naturopathy.html")


@app.route("/acupuncture")
def acupuncture():
    return render_template("acupuncture.html")


@app.route("/physiotherapy")
def physiotherapy():
    return render_template("physiotherapy.html")


@app.route("/nutrition-therapy")
def nutrition():
    return render_template("nutrition-therapy.html")


@app.route("/mental-health")
def mental():
    return render_template("mental-health.html")


@app.route("/disease/<disease_id>")
def disease_details(disease_id):
    return render_template("disease-details.html")

@app.route("/recommendation", methods=["GET"])
def recommendation():


    search_text = request.args.get("disease", "").strip()
    session["disease_name"] = search_text

    result = disease_df[
        disease_df["Disease_Name"].str.lower() == search_text.lower()
    ]

    if result.empty:

        symptom_match = symptoms_df[
            symptoms_df["Symptom"].str.lower().str.contains(search_text.lower(), na=False)
        ]

        if not symptom_match.empty:

            disease_id = symptom_match.iloc[0]["Disease_ID"]

            result = disease_df[
                disease_df["Disease_ID"] == disease_id
            ]

    if result.empty:
        return render_template(
            "recommendation.html",
            disease_name="Disease Not Found",
            category="-",
            body_system="-",
            severity="-"
        )

    disease = result.iloc[0]

    disease = result.iloc[0]
    disease_id = disease["Disease_ID"]
    body_result = body_df[ 
        body_df["Body_System_ID"] == disease["Body_System_ID"]
    ]

    body_system = "Unknown"

    if not body_result.empty:
        body_system = body_result.iloc[0]["Body_System"]
    
    symptom_result = symptoms_df[
    symptoms_df["Disease_ID"] == disease_id
    ]
    symptoms_html = ""

    for _, row in symptom_result.iterrows():
        symptoms_html += f"""
        <div class='flex justify-between border-b py-2'>
            <span>{row['Symptom']}</span>
            <span>{row['Type']}</span>
        </div>
        """
    if symptom_result.empty:
        symptoms_html = "<p>No symptoms available.</p>"
#PHASE 1
    diagnosis_result = diagnosis_df[
    diagnosis_df["Disease_ID"] == disease_id
    ]

    diagnosis_html = ""

    for _, row in diagnosis_result.iterrows():
        diagnosis_html += f"""
        <div class='border rounded-lg p-3 mb-2 bg-white'>
            <h4 class='font-semibold'>{row['Medical_Test']}</h4>
            <p class='text-gray-600'>{row['Purpose']}</p>
    </div>
    """
    if diagnosis_result.empty:
        diagnosis_html = "<p>No diagnostic tests available.</p>"

#PHASE 2
    medicine_result = medicine_df[
    medicine_df["Disease_ID"] == disease_id
]

    medicine_html = ""

    for _, row in medicine_result.iterrows():
        medicine_html += f"""
        <div class='border rounded-lg p-3 mb-2'>
            <h4 class='font-semibold'>{row['Medicine']}</h4>
            <p><b>Generic:</b> {row['Generic_Name']}</p>
            <p><b>Purpose:</b> {row['Purpose']}</p>
            <p><b>Dosage Form:</b> {row['Dosage_Form']}</p>
            <p><b>Side Effects:</b> {row['Side_Effects']}</p>
        </div>
        """
#PHASE 3
    primary = primary_treatment_df[
    primary_treatment_df["Disease_ID"] == disease_id
]

    primary_treatment = "Not Available"

    if not primary.empty:
        primary_treatment = primary.iloc[0]["Primary_Treatment"]
#PHASE 4
    diet = diet_df[
    diet_df["Disease_ID"] == disease_id
]

    eat = "Not Available"
    avoid = "Not Available"
    water = "Not Available"

    if not diet.empty:
        eat = diet.iloc[0]["Eat"]
        avoid = diet.iloc[0]["Avoid"]
        water = diet.iloc[0]["Water_Intake"]
##PHASE 5
    exercise = exercise_df[
    exercise_df["Disease_ID"] == disease_id
]

    exercise_text = ""
    yoga_text = ""

    if not exercise.empty:
        exercise_text = (
            f"{exercise.iloc[0]['Exercise']} "
            f"({exercise.iloc[0]['Duration']})"
        )

        yoga_text = (
            f"{exercise.iloc[0]['Yoga']} "
            f"({exercise.iloc[0]['Difficulty']})"
    )
    # PHASE 8 - Supportive Treatments

    supportive = supportive_treatment_df[
        supportive_treatment_df["Disease_ID"] == disease_id
]

    supportive_data = {}

    for _, row in supportive.iterrows():
        system = str(row["Treatment_System"]).strip()
        recommendation = str(row["Recommendation"]).strip()

        supportive_data[system] = recommendation
        print("Disease ID:", disease_id)
        print("Supportive Data:", supportive_data)

    print("Supportive Data:", supportive_data)
#PHASE 6
    prevention = prevention_df[
    prevention_df["Disease_ID"] == disease_id
]

    prevention_text = ""

    if not prevention.empty:
        prevention_text = prevention.iloc[0]["Prevention"]
#PHASE 7
    emergency = emergency_df[
    emergency_df["Disease_ID"] == disease_id
]

    warning = ""
    action = ""

    if not emergency.empty:
        warning = emergency.iloc[0]["Warning_Signs"]
        action = emergency.iloc[0]["Emergency_Action"]
        session["report"] = {
    "disease_name": disease["Disease_Name"],
    "category": disease["Category"],
    "body_system": body_system,
    "severity": disease["Severity"],
    "description": disease["Description"],

    "symptoms": symptoms_html,
    "diagnostic_procedures": diagnosis_html,
    "medicines": medicine_html,
    "primary_treatment": primary_treatment,

    "supportive_treatment_modern": supportive_data.get("Modern Medicine", "Not Available"),
    "supportive_treatment_ayurveda": supportive_data.get("Ayurveda", "Not Available"),
    "supportive_treatment_siddha": supportive_data.get("Siddha", "Not Available"),
    "supportive_treatment_homeopathy": supportive_data.get("Homeopathy", "Not Available"),
    "supportive_treatment_naturopathy": supportive_data.get("Naturopathy", "Not Available"),
    "supportive_treatment_acupuncture": supportive_data.get("Acupuncture", "Not Available"),
    "supportive_treatment_physiotherapy": supportive_data.get("Physiotherapy", "Not Available"),
    "supportive_treatment_nutrition": supportive_data.get("Nutrition Therapy", "Not Available"),
    "supportive_treatment_yoga": supportive_data.get("Yoga", "Not Available"),
    "supportive_treatment_mental_health": supportive_data.get("Mental Health", "Not Available"),

    "diet_recommended": eat,
    "diet_avoid": avoid,
    "water_intake": water,

    "exercises": exercise_text,
    "yoga_asanas": yoga_text,

    "prevention_tips": prevention_text,

    "emergency_symptoms": warning,
    "when_to_seek_help": action,

    "medical_disclaimer": "This information is for educational purposes only."
}
    return render_template(
            "recommendation.html",

        disease_name=disease["Disease_Name"],
        category=disease["Category"],
        body_system=body_system,
        severity=disease["Severity"],
        description=disease["Description"],

        # Temporary placeholders
        symptoms=symptoms_html,
        diagnostic_procedures=diagnosis_html,
        medicines=medicine_html,
        primary_treatment=primary_treatment,


        supportive_treatment_modern=supportive_data.get("Modern Medicine", "Recommended"),
        supportive_treatment_ayurveda=supportive_data.get("Ayurveda", "Not Available"),
        supportive_treatment_siddha=supportive_data.get("Siddha", "Not Available"),
        supportive_treatment_homeopathy=supportive_data.get("Homeopathy", "Not Available"),
        supportive_treatment_naturopathy=supportive_data.get("Naturopathy", "Not Available"),
        supportive_treatment_acupuncture=supportive_data.get("Acupuncture", "Not Available"),
        supportive_treatment_physiotherapy=supportive_data.get("Physiotherapy", "Not Available"),
        supportive_treatment_nutrition=supportive_data.get("Nutrition Therapy", "Not Available"),
        supportive_treatment_yoga=supportive_data.get("Yoga", "Not Available"),
        supportive_treatment_mental_health=supportive_data.get("Mental Health", "Not Available"),

        diet_recommended=eat,
        diet_avoid=avoid,
        water_intake=water,

        exercises=exercise_text,
        yoga_asanas=yoga_text,

        prevention_tips=prevention_text,

        emergency_symptoms=warning,
        when_to_seek_help=action,

        medical_disclaimer="This information is for educational purposes only. Always consult a qualified healthcare professional."
    )
@app.route("/body-systems")
def body_systems():
    return render_template("body_systems.html")

from flask import jsonify

@app.route("/search")
def search():
    q = request.args.get("q", "").lower().strip()

    if not q:
        return jsonify([])

    # disease match
    disease_match = disease_df[
        disease_df["Disease_Name"].str.lower().str.contains(q, na=False)
    ]

    # symptom match
    symptom_match = symptoms_df[
        symptoms_df["Symptom"].str.lower().str.contains(q, na=False)
    ]

    # collect disease names
    disease_names = disease_match["Disease_Name"].dropna().tolist()

    # convert symptoms → related diseases
    symptom_disease_ids = symptom_match["Disease_ID"].dropna().unique()

    symptom_disease_names = disease_df[
        disease_df["Disease_ID"].isin(symptom_disease_ids)
    ]["Disease_Name"].dropna().tolist()

    # merge + remove duplicates
    results = list(set(disease_names + symptom_disease_names))

    return jsonify(results)

import pdfkit
from flask import make_response, render_template

path_wkhtmltopdf = PATH_OF_THIS
config = pdfkit.configuration(PASS)

from playwright.sync_api import sync_playwright
from flask import send_file
@app.route("/ai-assistant")
def ai_assistant():
    return render_template("ai-assistant.html")

from flask import jsonify

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    message = data["message"]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message
    )

    return jsonify({
        "reply": response.text
    })
@app.route("/bmi-calculator")
def bmi_calculator():
    return render_template("bmi.html")


@app.route("/water-intake")
def water_intake():
    return render_template("water-intake.html")


@app.route("/calorie-calculator")
def calorie_calculator():
    return render_template("calorie.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():

    email = request.form["email"]

    sender_email = "YOUR_EMAIL"
    sender_password = "YOUR_PASS"

    receiver_email = "RECEIVER_EMAIL"

    subject = "New HealSphere Subscriber"

    body = f"""
A new user subscribed to HealSphere.

Subscriber Email:

{email}
"""

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()

        server.login(sender_email,sender_password)

        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string()
        )

        server.quit()

        return "<script>alert('Thank you for subscribing!');window.history.back();</script>"

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

